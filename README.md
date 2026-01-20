# SysMon - Server Tamagotchi 🖥️🐾

A gamified server monitoring tool that visualizes your system health through a Tamagotchi-like creature.

![SysMon Screenshot](https://github.com/PeterPage2115/SysMon/blob/92900139dc62e5c820b41878efdc2ebac0384ad7/icon.png)

## Features

- 🎮 **Gamified Monitoring** - Server pet with levels, XP, and health based on system metrics
- 📊 **Real-time Stats** - WebSocket updates every 2 seconds for CPU, RAM, disk, and Docker containers
- 🐳 **Docker Integration** - Monitor container health via Docker SDK
- 💾 **Persistent State** - SQLite database saves your Tamagotchi's progress
- 🎨 **Beautiful UI** - Gradient-rich Svelte frontend with responsive design

## Quick Start (Docker Compose)

```bash
# Clone the repository
git clone https://github.com/PeterPage2115/SysMon.git
cd SysMon

# Start the container
docker-compose up -d

# Access the WebUI
open http://localhost:8000
```

### Unraid Users

The `docker-compose.yml` is pre-configured with:
- `--pid=host` for real host metrics (not container stats)
- Docker socket access for container monitoring
- Persistent data volume

Just run `docker-compose up -d` and access `http://YOUR-UNRAID-IP:8000`.

## How It Works

Your Tamagotchi's mood reflects server health:
- 😊 **Happy** - Low resource usage (< 50%)
- 😐 **Neutral** - Moderate usage (50-80%)  
- 😰 **Stressed** - High usage (80-95%)
- 🤒 **Critical** - Overloaded (> 95%)

Feed your pet to gain XP and level up!

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check with version info |
| `/api/stats` | GET | Current system statistics |
| `/api/tamagotchi` | GET | Tamagotchi state |
| `/api/tamagotchi/rename?name=X` | POST | Rename your pet |
| `/api/tamagotchi/feed` | POST | Feed for +10 XP |
| `/ws` | WebSocket | Real-time updates |

## Tech Stack

- **Backend**: Python 3.11, FastAPI, WebSockets, psutil, Docker SDK
- **Frontend**: Svelte 4, Vite
- **Database**: SQLite (SQLModel)
- **Deployment**: Docker (multi-stage build)

## Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend  
cd frontend
npm install
npm run dev
```

## License

MIT

## Contributing

Pull requests welcome!
