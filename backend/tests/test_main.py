"""Tests for FastAPI main application."""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_session


@pytest.fixture
def client(session, mock_system_monitor):
    """Create a test client with mocked dependencies."""
    def get_session_override():
        yield session
    
    app.dependency_overrides[get_session] = get_session_override
    
    # Re-initialize SystemMonitor with mocked dependencies
    from app.main import monitor
    monitor.__init__()
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "SysMon"


def test_get_stats(client, mock_system_monitor):
    """Test system stats endpoint."""
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    
    # Verify structure
    assert "cpu_percent" in data
    assert "memory_percent" in data
    assert "memory_used_gb" in data
    assert "memory_total_gb" in data
    assert "disk_percent" in data
    assert "disk_used_gb" in data
    assert "disk_total_gb" in data
    assert "docker_containers_total" in data
    assert "docker_containers_running" in data
    assert "docker_containers_stopped" in data
    assert "timestamp" in data
    
    # Verify mocked values
    assert data["cpu_percent"] == 45.5
    assert data["memory_percent"] == 60.2
    assert data["docker_containers_total"] == 4
    assert data["docker_containers_running"] == 3
    assert data["docker_containers_stopped"] == 1


def test_get_tamagotchi(client):
    """Test get Tamagotchi endpoint."""
    response = client.get("/api/tamagotchi")
    assert response.status_code == 200
    data = response.json()
    
    # Verify structure
    assert "id" in data
    assert "name" in data
    assert "level" in data
    assert "xp" in data
    assert "health" in data
    assert "happiness" in data
    
    # Verify defaults
    assert data["name"] == "Server-chan"
    assert data["level"] >= 1
    assert data["xp"] >= 0
    assert 0 <= data["health"] <= 100
    assert 0 <= data["happiness"] <= 100


def test_rename_tamagotchi(client):
    """Test rename Tamagotchi endpoint."""
    new_name = "TestBot-2000"
    response = client.post(f"/api/tamagotchi/rename?name={new_name}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_name


def test_feed_tamagotchi(client):
    """Test feed Tamagotchi endpoint."""
    # Get initial state
    response = client.get("/api/tamagotchi")
    initial = response.json()
    initial_xp = initial["xp"]
    initial_happiness = initial["happiness"]
    
    # Feed the Tamagotchi
    response = client.post("/api/tamagotchi/feed")
    assert response.status_code == 200
    data = response.json()
    
    # Verify XP increased
    assert data["xp"] == initial_xp + 10 or data["level"] > initial["level"]
    
    # Verify happiness increased (up to max 100)
    assert data["happiness"] >= initial_happiness


@pytest.mark.asyncio
async def test_websocket_connection(client, mock_system_monitor):
    """Test WebSocket connection and message format."""
    import json
    
    with client.websocket_connect("/ws") as websocket:
        # Send a test message
        websocket.send_text("ping")
        
        # Receive response
        data = websocket.receive_text()
        assert "Message received: ping" in data


@pytest.mark.asyncio
async def test_websocket_disconnect(client, mock_system_monitor):
    """Test WebSocket disconnection handling."""
    with client.websocket_connect("/ws") as websocket:
        # Close connection
        websocket.close()
    
    # Connection should close gracefully without errors
    assert True
