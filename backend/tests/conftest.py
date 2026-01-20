"""Test configuration and fixtures for SysMon tests."""
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.database import get_session
from app.models import Tamagotchi  # Import models before creating tables


@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session


@pytest.fixture
def mock_system_monitor(monkeypatch):
    """Mock psutil and docker for testing without host access."""
    from unittest.mock import MagicMock, Mock
    
    # Mock psutil
    mock_psutil = MagicMock()
    mock_psutil.cpu_percent.return_value = 45.5
    mock_psutil.virtual_memory.return_value = Mock(
        percent=60.2,
        used=8 * (1024 ** 3),  # 8 GB
        total=16 * (1024 ** 3)  # 16 GB
    )
    mock_psutil.disk_usage.return_value = Mock(
        percent=70.0,
        used=700 * (1024 ** 3),  # 700 GB
        total=1000 * (1024 ** 3)  # 1000 GB (1 TB)
    )
    
    # Mock docker APIClient
    mock_api_client = MagicMock()
    # APIClient.containers() returns list of dicts, not objects
    mock_api_client.containers.return_value = [
        {"State": "running", "Id": "abc123"},
        {"State": "running", "Id": "def456"},
        {"State": "running", "Id": "ghi789"},
        {"State": "exited", "Id": "jkl012"},
    ]
    mock_api_client.version.return_value = {"Version": "24.0.0"}
    
    mock_docker = MagicMock()
    # Mock APIClient constructor
    mock_docker.APIClient.return_value = mock_api_client
    
    # Apply mocks - patch modules where they're used
    monkeypatch.setattr("app.services.system_monitor.psutil.cpu_percent", mock_psutil.cpu_percent)
    monkeypatch.setattr("app.services.system_monitor.psutil.virtual_memory", mock_psutil.virtual_memory)
    monkeypatch.setattr("app.services.system_monitor.psutil.disk_usage", mock_psutil.disk_usage)
    monkeypatch.setattr("app.services.system_monitor.docker.APIClient", mock_docker.APIClient)
    
    return {
        "psutil": mock_psutil,
        "api_client": mock_api_client
    }
