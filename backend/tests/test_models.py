"""Tests for database models."""
import pytest
from datetime import datetime
from app.models import Tamagotchi, SystemStats


def test_tamagotchi_creation(session):
    """Test creating a Tamagotchi."""
    tamagotchi = Tamagotchi(name="TestBot", level=5, xp=250)
    session.add(tamagotchi)
    session.commit()
    session.refresh(tamagotchi)
    
    assert tamagotchi.id is not None
    assert tamagotchi.name == "TestBot"
    assert tamagotchi.level == 5
    assert tamagotchi.xp == 250
    assert tamagotchi.health == 100.0
    assert tamagotchi.happiness == 100.0
    assert isinstance(tamagotchi.created_at, datetime)
    assert isinstance(tamagotchi.updated_at, datetime)


def test_tamagotchi_defaults(session):
    """Test Tamagotchi default values."""
    tamagotchi = Tamagotchi()
    session.add(tamagotchi)
    session.commit()
    session.refresh(tamagotchi)
    
    assert tamagotchi.name == "Server-chan"
    assert tamagotchi.level == 1
    assert tamagotchi.xp == 0
    assert tamagotchi.health == 100.0
    assert tamagotchi.happiness == 100.0


def test_system_stats_model():
    """Test SystemStats model."""
    stats = SystemStats(
        timestamp=datetime.utcnow(),
        cpu_percent=45.5,
        memory_percent=60.2,
        memory_used_gb=8.0,
        memory_total_gb=16.0,
        disk_percent=70.0,
        disk_used_gb=700.0,
        disk_total_gb=1000.0,
        docker_containers_total=4,
        docker_containers_running=3,
        docker_containers_stopped=1
    )
    
    assert stats.cpu_percent == 45.5
    assert stats.memory_percent == 60.2
    assert stats.docker_containers_total == 4
    
    # Test model_dump (Pydantic v2)
    data = stats.model_dump()
    assert isinstance(data, dict)
    assert data["cpu_percent"] == 45.5
