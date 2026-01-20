# SysMon - Server Tamagotchi 🖥️🐾

A cute server monitoring tool that visualizes your system health through a Tamagotchi-like creature. Built with Python FastAPI, WebSockets, and Svelte.

## Features

- 🎮 **Gamified Monitoring**: Server pet with levels, XP, and health based on system metrics
- 📊 **Real-time Stats**: WebSocket updates every 2 seconds for CPU, RAM, disk, and Docker containers
- 🐳 **Docker Integration**: Monitor container health via Docker SDK
- 💾 **Persistent State**: SQLite database saves your Tamagotchi's progress
- 🎨 **Beautiful UI**: Gradient-rich Svelte frontend with responsive design
- 🏗️ **Single Container**: Optimized for Unraid deployment

## Project Structure

```
SysMon/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app + WebSocket broadcasting
│   │   ├── models.py            # SQLModel data models
│   │   ├── database.py          # SQLite session management
│   │   ├── services/
│   │   │   └── system_monitor.py  # psutil + Docker SDK metrics
│   │   └── websocket/
│   │       └── manager.py       # WebSocket connection manager
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.svelte
│   │   ├── lib/
│   │   │   ├── Tamagotchi.svelte
│   │   │   └── SystemStats.svelte
│   │   └── stores/
│   │       └── websocket.js     # WebSocket store with auto-reconnect
│   └── package.json
├── Dockerfile                   # Multi-stage build (Node + Python)
└── docker-compose.yml
```

## Unraid Deployment

### Requirements
- Unraid 6.9+
- Docker enabled

### Setup

1. **Clone or copy the project to your Unraid server**:
   ```bash
   cd /mnt/user/appdata
   git clone <your-repo> sysmon
   cd sysmon
   ```

2. **Build and run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

3. **Access the web UI**:
   - Navigate to `http://YOUR-UNRAID-IP:8000`

### Configuration

The [docker-compose.yml](docker-compose.yml) is pre-configured for Unraid:

- **`pid: host`** - Allows psutil to see host CPU/RAM (not container stats)
- **`/var/run/docker.sock`** - Docker SDK access for container monitoring
- **`./data`** - Persistent SQLite database (Tamagotchi state)

## Local Development

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` (frontend) and `http://localhost:8000` (backend).

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/stats` - Current system statistics
- `GET /api/tamagotchi` - Tamagotchi state
- `POST /api/tamagotchi/rename?name=NewName` - Rename your pet
- `POST /api/tamagotchi/feed` - Feed for +10 XP
- `WS /ws` - WebSocket for real-time updates

## How It Works

1. **Backend Loop**: [main.py](backend/app/main.py) runs `broadcast_system_stats()` as a background task
2. **Metrics Collection**: [system_monitor.py](backend/app/services/system_monitor.py) uses `psutil` and Docker SDK
3. **Broadcasting**: [manager.py](backend/app/websocket/manager.py) sends JSON to all connected WebSocket clients
4. **Frontend Store**: [websocket.js](frontend/src/stores/websocket.js) auto-connects and updates Svelte components
5. **Tamagotchi Logic**: Health score calculated from CPU/RAM/disk/Docker stats

## Health Score Algorithm

```python
health = (
    (100 - cpu_percent) * 0.3 +
    (100 - memory_percent) * 0.3 +
    (100 - disk_percent) * 0.2 +
    min(100, running_containers * 10) * 0.2
)
```

Lower resource usage = happier pet! 😊

## License

MIT

## Contributing

Pull requests welcome! This is a fun project to learn FastAPI, WebSockets, and Svelte.
