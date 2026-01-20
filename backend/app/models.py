"""Database models for SysMon Tamagotchi."""
from __future__ import annotations  # PEP 563 - deferred annotations for Python 3.14 compatibility
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Tamagotchi(SQLModel, table=True):
    """Tamagotchi state - name, level, XP for gamification."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default="Server-chan", max_length=50)
    level: int = Field(default=1, ge=1)
    xp: int = Field(default=0, ge=0)
    health: float = Field(default=100.0, ge=0.0, le=100.0)
    happiness: float = Field(default=100.0, ge=0.0, le=100.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class SystemStats(SQLModel):
    """System statistics snapshot (not stored, just for API response)."""
    
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_used_gb: float
    memory_total_gb: float
    disk_percent: float
    disk_used_gb: float
    disk_total_gb: float
    docker_containers_total: int
    docker_containers_running: int
    docker_containers_stopped: int
