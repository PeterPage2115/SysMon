"""FastAPI main application - serves API and static Svelte frontend."""
import asyncio
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlmodel import Session, select

from app.database import init_db, get_session, engine
from app.models import Tamagotchi, SystemStats
from app.services.system_monitor import SystemMonitor
from app.websocket.manager import ConnectionManager

# Read version from VERSION file (check multiple locations for dev vs container)
VERSION_FILE_LOCATIONS = [
    Path("/app/VERSION"),  # Container path (Dockerfile: COPY VERSION /app/VERSION)
    Path(__file__).parent.parent.parent / "VERSION",  # Dev path
]
VERSION = "dev"
for version_file in VERSION_FILE_LOCATIONS:
    if version_file.exists():
        VERSION = version_file.read_text().strip()
        break

# Initialize components
monitor = SystemMonitor()
manager = ConnectionManager()


# Background task for broadcasting stats
async def broadcast_system_stats():
    """Background task: collect and broadcast stats every 2 seconds."""
    print("✓ Started background stats broadcaster")
    
    while True:
        try:
            # Collect system stats
            stats = monitor.get_stats()
            health_score = monitor.get_health_score(stats)
            
            # Update Tamagotchi health in database
            with Session(engine) as session:
                tamagotchi = session.exec(select(Tamagotchi)).first()
                if tamagotchi:
                    tamagotchi.health = health_score
                    session.add(tamagotchi)
                    session.commit()
                    session.refresh(tamagotchi)
                    
                    # Broadcast to all connected clients
                    # Convert stats to dict with ISO timestamp
                    stats_dict = stats.model_dump()
                    stats_dict["timestamp"] = stats.timestamp.isoformat()
                    
                    message = {
                        "type": "stats_update",
                        "stats": stats_dict,
                        "tamagotchi": {
                            "name": tamagotchi.name,
                            "level": tamagotchi.level,
                            "xp": tamagotchi.xp,
                            "health": tamagotchi.health,
                            "happiness": tamagotchi.happiness
                        }
                    }
                    
                    if manager.get_connection_count() > 0:
                        await manager.broadcast(message)
            
        except Exception as e:
            print(f"⚠ Error in broadcast loop: {e}")
        
        # Wait 2 seconds before next broadcast
        await asyncio.sleep(2)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    print(f"🚀 Starting SysMon v{VERSION}...")
    init_db()
    
    # Ensure Tamagotchi exists
    with Session(engine) as session:
        tamagotchi = session.exec(select(Tamagotchi)).first()
        if not tamagotchi:
            tamagotchi = Tamagotchi()
            session.add(tamagotchi)
            session.commit()
            print("✓ Created initial Tamagotchi")
    
    # Start background stats broadcaster
    task = asyncio.create_task(broadcast_system_stats())
    
    yield
    
    # Shutdown
    print("🛑 Shutting down SysMon...")
    task.cancel()


# Create FastAPI app
app = FastAPI(
    title="SysMon - Server Tamagotchi",
    description="Monitor your server health through a cute Tamagotchi creature",
    version="1.0.0",
    lifespan=lifespan
)


# API Routes
@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy", 
        "service": "SysMon",
        "version": VERSION,
        "docker_available": monitor.docker_available
    }


@app.get("/api/stats")
async def get_stats():
    """Get current system stats."""
    stats = monitor.get_stats()
    return stats.model_dump()


@app.get("/api/tamagotchi")
async def get_tamagotchi(session: Annotated[Session, Depends(get_session)]):
    """Get Tamagotchi state."""
    tamagotchi = session.exec(select(Tamagotchi)).first()
    if not tamagotchi:
        tamagotchi = Tamagotchi()
        session.add(tamagotchi)
        session.commit()
        session.refresh(tamagotchi)
    return tamagotchi


@app.post("/api/tamagotchi/rename")
async def rename_tamagotchi(
    name: str,
    session: Annotated[Session, Depends(get_session)]
):
    """Rename the Tamagotchi."""
    tamagotchi = session.exec(select(Tamagotchi)).first()
    if not tamagotchi:
        tamagotchi = Tamagotchi(name=name)
        session.add(tamagotchi)
        session.commit()
        session.refresh(tamagotchi)
        return tamagotchi
    
    tamagotchi.name = name
    session.add(tamagotchi)
    session.commit()
    session.refresh(tamagotchi)
    return tamagotchi


@app.post("/api/tamagotchi/feed")
async def feed_tamagotchi(session: Annotated[Session, Depends(get_session)]):
    """Feed the Tamagotchi (gain XP)."""
    tamagotchi = session.exec(select(Tamagotchi)).first()
    if tamagotchi:
        tamagotchi.xp += 10
        tamagotchi.happiness = min(100, tamagotchi.happiness + 5)
        
        # Level up every 100 XP
        if tamagotchi.xp >= tamagotchi.level * 100:
            tamagotchi.level += 1
            tamagotchi.xp = 0
        
        session.add(tamagotchi)
        session.commit()
        session.refresh(tamagotchi)
        return tamagotchi
    return {"error": "Tamagotchi not found"}


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time stats updates."""
    await manager.connect(websocket)
    
    try:
        # Keep connection alive - broadcast loop will send data
        while True:
            try:
                # Wait for client messages with a timeout
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                # Echo back for testing
                await manager.send_personal_message(f"Message received: {data}", websocket)
            except asyncio.TimeoutError:
                # Send ping to keep connection alive
                await websocket.send_json({"type": "ping"})
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"⚠ WebSocket error: {e}")
        manager.disconnect(websocket)


# Serve static frontend files (built Svelte app)
# Mount static files after API routes
static_dir = Path(__file__).parent.parent / "frontend" / "dist"

if static_dir.exists():
    app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve Svelte frontend."""
        # Try to serve the requested file
        file_path = static_dir / full_path
        
        if file_path.is_file():
            return FileResponse(file_path)
        
        # Otherwise serve index.html (SPA fallback)
        return FileResponse(static_dir / "index.html")
else:
    print("⚠ Frontend dist/ directory not found. Run: cd frontend && npm run build")
    
    @app.get("/")
    async def root():
        return {
            "message": "Frontend not built yet",
            "instructions": "Run: cd frontend && npm install && npm run build"
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
