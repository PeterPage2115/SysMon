"""Tests for WebSocket connection manager."""
import pytest
from fastapi import WebSocket
from unittest.mock import AsyncMock, MagicMock
from app.websocket.manager import ConnectionManager


@pytest.mark.asyncio
async def test_connect():
    """Test WebSocket connection."""
    manager = ConnectionManager()
    websocket = MagicMock(spec=WebSocket)
    websocket.accept = AsyncMock()
    
    await manager.connect(websocket)
    
    assert websocket in manager.active_connections
    assert manager.get_connection_count() == 1
    websocket.accept.assert_called_once()


@pytest.mark.asyncio
async def test_disconnect():
    """Test WebSocket disconnection."""
    manager = ConnectionManager()
    websocket = MagicMock(spec=WebSocket)
    websocket.accept = AsyncMock()
    
    await manager.connect(websocket)
    manager.disconnect(websocket)
    
    assert websocket not in manager.active_connections
    assert manager.get_connection_count() == 0


@pytest.mark.asyncio
async def test_send_personal_message():
    """Test sending message to specific client."""
    manager = ConnectionManager()
    websocket = MagicMock(spec=WebSocket)
    websocket.accept = AsyncMock()
    websocket.send_text = AsyncMock()
    
    await manager.connect(websocket)
    await manager.send_personal_message("test message", websocket)
    
    websocket.send_text.assert_called_once_with("test message")


@pytest.mark.asyncio
async def test_broadcast():
    """Test broadcasting to multiple clients."""
    manager = ConnectionManager()
    
    websocket1 = MagicMock(spec=WebSocket)
    websocket1.accept = AsyncMock()
    websocket1.send_text = AsyncMock()
    
    websocket2 = MagicMock(spec=WebSocket)
    websocket2.accept = AsyncMock()
    websocket2.send_text = AsyncMock()
    
    await manager.connect(websocket1)
    await manager.connect(websocket2)
    
    message = {"type": "test", "data": "hello"}
    await manager.broadcast(message)
    
    # Both clients should receive the message
    assert websocket1.send_text.call_count == 1
    assert websocket2.send_text.call_count == 1


@pytest.mark.asyncio
async def test_broadcast_with_failed_connection():
    """Test broadcast removes failed connections."""
    manager = ConnectionManager()
    
    # Working connection
    websocket1 = MagicMock(spec=WebSocket)
    websocket1.accept = AsyncMock()
    websocket1.send_text = AsyncMock()
    
    # Failing connection
    websocket2 = MagicMock(spec=WebSocket)
    websocket2.accept = AsyncMock()
    websocket2.send_text = AsyncMock(side_effect=Exception("Connection lost"))
    
    await manager.connect(websocket1)
    await manager.connect(websocket2)
    
    assert manager.get_connection_count() == 2
    
    message = {"type": "test", "data": "hello"}
    await manager.broadcast(message)
    
    # Failed connection should be removed
    assert manager.get_connection_count() == 1
    assert websocket1 in manager.active_connections
    assert websocket2 not in manager.active_connections
