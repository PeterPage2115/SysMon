# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-01-20

### Fixed
- **Docker SDK Unix Socket**: Fixed "Not supported URL scheme http+docker" error by pinning `requests<2.32.0` (compatibility issue with requests 2.32.2+ API change)
- **WebSocket Stability**: Removed blocking `psutil.cpu_percent(interval=1)` call from WebSocket endpoint; now runs in thread pool via `asyncio.to_thread()`
- **Svelte Store Access**: Fixed incorrect store destructuring in App.svelte that caused "Disconnected" status and no data display
- **JSON Serialization**: Fixed "Object of type datetime is not JSON serializable" error by converting timestamps to ISO format
- **Host Disk Monitoring**: Added configurable `DISK_PATH` environment variable to monitor host disk instead of container filesystem
- **Dockerfile Cleanup**: Removed references to deleted test files

### Changed
- **Docker SDK**: Downgraded from 7.0.0 to 6.1.3 for better Unix socket compatibility
- **Broadcast Loop**: Now uses `asyncio.to_thread()` for non-blocking stats collection
- **Startup**: Tamagotchi is now created automatically on application startup
- **Docker Compose**: Updated to use `latest` tag and added host disk mount (`/mnt/user:/host/mnt/user:ro`)

### Removed
- Removed obsolete documentation files (DEPLOY_UNRAID.md, FORCE_UPDATE_UNRAID.md, UPDATE_UNRAID.md)
- Removed diagnostic test scripts (simple_test.py, test_container_env.py, test_docker_sdk.py)

### Technical Details
- Added broadcast logging ("📡 Broadcasting to X client(s)...")
- Improved error handling in WebSocket endpoint
- Environment variable `DISK_PATH` defaults to `/` with fallback on error

## [0.1.0] - 2026-01-20

### Added
- **Server Tamagotchi Monitoring**: Gamified server health visualization through a Tamagotchi-like creature
- **FastAPI Backend**: RESTful API with WebSocket support for real-time system metrics
  - `/api/health` - Health check endpoint
  - `/api/stats` - Current system statistics (CPU, RAM, disk, Docker containers)
  - `/api/tamagotchi` - Tamagotchi state (name, level, XP, health, happiness)
  - `/api/tamagotchi/rename` - Rename your Tamagotchi
  - `/api/tamagotchi/feed` - Feed Tamagotchi to gain XP and happiness
  - `/ws` - WebSocket endpoint for real-time metrics broadcasting
- **System Monitoring**: 
  - CPU usage monitoring with psutil
  - RAM usage (used/total in GB, percentage)
  - Disk usage (used/total in GB, percentage)
  - Docker container tracking (total/running/stopped)
  - Health score calculation based on system metrics
- **Svelte Frontend**:
  - Animated Tamagotchi creature with mood indicators (😊/😐/😰/🤒)
  - Real-time system stats dashboard with progress bars
  - Feed button with XP/level progression
  - Rename functionality
  - WebSocket connection with auto-reconnect
  - Connection status indicator
- **Gamification Features**:
  - XP system with level progression (100 XP per level)
  - Health score influenced by system performance
  - Happiness mechanics tied to system health
  - Dynamic mood based on server health
- **Docker Deployment**:
  - Multi-stage Dockerfile for optimized image size
  - Single-container architecture (frontend + backend)
  - Unraid-optimized with `--pid=host` support
  - SQLite persistence with volume mounting
  - Docker socket mounting for container monitoring
- **CI/CD Pipeline**:
  - GitHub Actions workflow for automated builds
  - Automatic Docker image push to Docker Hub
  - Build caching for faster CI builds
  - Multi-architecture support preparation
- **Comprehensive Testing**:
  - 19 passing unit tests with pytest
  - Mocked psutil and Docker SDK for isolated testing
  - API endpoint tests with FastAPI TestClient
  - WebSocket connection/broadcast tests
  - Model validation tests
  - System monitor health calculation tests
- **Documentation**:
  - Unraid deployment guide (DEPLOY_UNRAID.md)
  - README with project overview
  - Copilot instructions for project structure
  - Docker Compose configuration example
  - Environment configuration template

### Fixed
- Python 3.14 compatibility with Pydantic/SQLModel using `from __future__ import annotations`
- Package-lock.json added for deterministic npm builds in CI/CD
- Rename endpoint now creates Tamagotchi if it doesn't exist
- Docker mock configuration in tests for proper container stats

### Technical Details
- **Backend Stack**: Python 3.11+, FastAPI 0.109.0, SQLModel 0.0.22, psutil 5.9.8, Docker SDK 7.0.0
- **Frontend Stack**: Svelte 4, Vite
- **Database**: SQLite with SQLModel ORM
- **Deployment**: Docker (multi-stage build), Docker Hub
- **Testing**: pytest 7.4.3, pytest-asyncio 0.21.1, httpx 0.25.2
- **CI/CD**: GitHub Actions with Docker Buildx

### Security
- Docker socket mounted read-only for security
- `--pid=host` provides process visibility without control
- No external API calls (all metrics are local)
- SQLite database has no remote access

### Performance
- WebSocket broadcasts every 2 seconds (configurable)
- Frontend uses Svelte stores for efficient reactivity
- Docker SDK API calls are cached
- Multi-stage build reduces final image size

[0.1.0]: https://github.com/PeterPage2115/SysMon/releases/tag/v0.1.0
