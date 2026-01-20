"""Tests for system monitoring service."""
import pytest
from app.services.system_monitor import SystemMonitor


def test_get_stats(mock_system_monitor):
    """Test getting system stats with mocked psutil and docker."""
    monitor = SystemMonitor()
    stats = monitor.get_stats()
    
    # Verify all fields are present
    assert stats.cpu_percent == 45.5
    assert stats.memory_percent == 60.2
    assert stats.memory_used_gb == 8.0
    assert stats.memory_total_gb == 16.0
    assert stats.disk_percent == 70.0
    assert stats.disk_used_gb == 700.0
    assert stats.disk_total_gb == 1000.0
    assert stats.docker_containers_total == 4
    assert stats.docker_containers_running == 3
    assert stats.docker_containers_stopped == 1
    assert stats.timestamp is not None


def test_health_score_calculation(mock_system_monitor):
    """Test health score calculation."""
    monitor = SystemMonitor()
    stats = monitor.get_stats()
    health = monitor.get_health_score(stats)
    
    # Health should be between 0 and 100
    assert 0 <= health <= 100
    
    # With our mock data (CPU: 45.5%, RAM: 60.2%, Disk: 70%, Docker: 3 running)
    # Expected: (54.5 * 0.3) + (39.8 * 0.3) + (30 * 0.2) + (30 * 0.2) = 40.29
    assert 35 <= health <= 45  # Allow some rounding tolerance


def test_docker_unavailable():
    """Test behavior when Docker is unavailable."""
    from unittest.mock import MagicMock
    
    # Create monitor with failing Docker client
    monitor = SystemMonitor()
    monitor.docker_client = None
    monitor.docker_available = False
    
    stats = monitor._get_docker_stats()
    
    # Should return zeros gracefully
    assert stats["total"] == 0
    assert stats["running"] == 0
    assert stats["stopped"] == 0


def test_docker_error_handling(mock_system_monitor, monkeypatch):
    """Test Docker API error handling."""
    from unittest.mock import MagicMock
    
    monitor = SystemMonitor()
    
    # Mock APIClient to raise exception
    def raise_error(*args, **kwargs):
        raise Exception("Docker daemon not available")
    
    monitor.api_client.containers = raise_error
    
    stats = monitor._get_docker_stats()
    
    # Should return zeros on error
    assert stats["total"] == 0
    assert stats["running"] == 0
    assert stats["stopped"] == 0
