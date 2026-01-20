"""System monitoring service using psutil and Docker SDK."""
import psutil
import docker
from datetime import datetime
from typing import Dict, Any
from app.models import SystemStats


class SystemMonitor:
    """Monitor system metrics (CPU, RAM, disk, Docker)."""
    
    def __init__(self):
        """Initialize Docker client."""
        try:
            # Use explicit socket path for Docker API  
            # Note: unix:/// requires 3 slashes for absolute path
            self.docker_client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
            self.docker_available = True
            print("✓ Docker SDK connected")
        except Exception as e:
            print(f"⚠ Docker SDK unavailable: {e}")
            self.docker_client = None
            self.docker_available = False
    
    def get_stats(self) -> SystemStats:
        """Collect all system statistics."""
        # CPU usage (averaged over 1 second)
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used_gb = memory.used / (1024 ** 3)
        memory_total_gb = memory.total / (1024 ** 3)
        
        # Disk usage (root partition)
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_used_gb = disk.used / (1024 ** 3)
        disk_total_gb = disk.total / (1024 ** 3)
        
        # Docker container stats
        docker_stats = self._get_docker_stats()
        
        return SystemStats(
            timestamp=datetime.utcnow(),
            cpu_percent=round(cpu_percent, 2),
            memory_percent=round(memory_percent, 2),
            memory_used_gb=round(memory_used_gb, 2),
            memory_total_gb=round(memory_total_gb, 2),
            disk_percent=round(disk_percent, 2),
            disk_used_gb=round(disk_used_gb, 2),
            disk_total_gb=round(disk_total_gb, 2),
            docker_containers_total=docker_stats["total"],
            docker_containers_running=docker_stats["running"],
            docker_containers_stopped=docker_stats["stopped"]
        )
    
    def _get_docker_stats(self) -> Dict[str, int]:
        """Get Docker container statistics."""
        if not self.docker_available:
            return {"total": 0, "running": 0, "stopped": 0}
        
        try:
            containers = self.docker_client.containers.list(all=True)
            running = sum(1 for c in containers if c.status == "running")
            stopped = sum(1 for c in containers if c.status in ["exited", "stopped"])
            
            return {
                "total": len(containers),
                "running": running,
                "stopped": stopped
            }
        except Exception as e:
            print(f"⚠ Error fetching Docker stats: {e}")
            return {"total": 0, "running": 0, "stopped": 0}
    
    def get_health_score(self, stats: SystemStats) -> float:
        """
        Calculate health score (0-100) based on system metrics.
        Lower resource usage = higher health.
        """
        # Invert percentages so low usage = high score
        cpu_health = max(0, 100 - stats.cpu_percent)
        memory_health = max(0, 100 - stats.memory_percent)
        disk_health = max(0, 100 - stats.disk_percent)
        
        # Docker health: running containers are good
        docker_health = min(100, stats.docker_containers_running * 10)
        
        # Weighted average
        health = (
            cpu_health * 0.3 +
            memory_health * 0.3 +
            disk_health * 0.2 +
            docker_health * 0.2
        )
        
        return round(health, 2)
