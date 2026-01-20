# 🐳 Unraid Deployment Guide - SysMon

This guide shows you how to deploy **SysMon** (Server Tamagotchi) on Unraid using Docker.

---

## 📋 Prerequisites

- Unraid 6.9 or newer
- Docker enabled in Unraid settings
- Community Applications plugin (optional, for easier installation)

---

## 🚀 Quick Installation via Unraid Docker UI

### Step 1: Open Docker Tab

Navigate to: **Docker → Add Container**

### Step 2: Configure Container

Fill in the following settings:

#### **Basic Settings**

| Field | Value |
|-------|-------|
| **Name** | `sysmon` |
| **Repository** | `peterpage2115/sysmon:latest` |
| **Network Type** | `Bridge` |

#### **Port Mappings**

| Container Port | Host Port | Description |
|----------------|-----------|-------------|
| `8000` | `8000` | WebUI Access |

> Access the UI at: `http://YOUR-UNRAID-IP:8000`

#### **Path Mappings (Volumes)**

| Container Path | Host Path | Access Mode | Description |
|----------------|-----------|-------------|-------------|
| `/var/run/docker.sock` | `/var/run/docker.sock` | **Read/Write** | Docker container monitoring |
| `/app/data` | `/mnt/user/appdata/sysmon` | Read/Write | SQLite database persistence |

⚠️ **CRITICAL**: The Docker socket mapping is **required** for container monitoring!

#### **Extra Parameters** ⚠️ MANDATORY

In the "Extra Parameters" field, add:

```
--pid=host
```

**Why is this needed?**  
The `--pid=host` flag allows the container to see your **Unraid server's actual CPU and RAM usage**, not just the container's isolated metrics. Without this, SysMon would only monitor its own tiny resource footprint instead of your entire server.

#### **Environment Variables** (Optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./data/sysmon.db` | Database connection string |

---

## 🖼️ Visual Configuration Summary

Your Unraid Docker configuration should look like this:

```
Container Name: sysmon
Repository: peterpage2115/sysmon:latest
Network Type: Bridge

Port Mappings:
  8000 → 8000

Volume Mappings:
  /var/run/docker.sock → /var/run/docker.sock (RW)
  /app/data → /mnt/user/appdata/sysmon (RW)

Extra Parameters:
  --pid=host
```

---

## 🎬 Post-Installation

1. **Start the container**:
   - Click "Apply" in the Docker UI
   - Wait for the image to download (~150 MB)

2. **Access the WebUI**:
   - Navigate to: `http://YOUR-UNRAID-IP:8000`
   - You should see your Server Tamagotchi!

3. **Verify it's working**:
   - Check that CPU/RAM stats match your Unraid dashboard
   - Verify Docker container counts are accurate
   - Try feeding your Tamagotchi (bottom button)

---

## 🔧 Manual Installation via Command Line

If you prefer the terminal:

```bash
docker run -d \
  --name=sysmon \
  --pid=host \
  -p 8000:8000 \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /mnt/user/appdata/sysmon:/app/data \
  -e DATABASE_URL=sqlite:///./data/sysmon.db \
  --restart=unless-stopped \
  peterpage2115/sysmon:latest
```

---

## 📊 What Gets Monitored

SysMon tracks:

- ✅ **CPU Usage** - Host CPU percentage
- ✅ **RAM Usage** - Host memory consumption
- ✅ **Disk Usage** - Root filesystem
- ✅ **Docker Containers** - Total, running, and stopped containers

The Tamagotchi's health reflects your server's resource usage:
- 😊 **Happy** - Low resource usage (< 50%)
- 😐 **Neutral** - Moderate usage (50-80%)
- 😰 **Stressed** - High usage (80-95%)
- 🤒 **Critical** - Overloaded (> 95%)

---

## 🔄 Updating SysMon

To update to the latest version:

1. **Via Unraid UI**:
   - Go to Docker tab
   - Click "Check for Updates"
   - Click "Update" next to SysMon

2. **Via Command Line**:
   ```bash
   docker stop sysmon
   docker rm sysmon
   docker pull peterpage2115/sysmon:latest
   # Then run the docker run command again
   ```

---

## 🐛 Troubleshooting

### Container shows wrong CPU/RAM stats

**Problem**: SysMon shows ~1% CPU and 200 MB RAM instead of actual server stats.

**Solution**: Add `--pid=host` to Extra Parameters. This is **mandatory**!

### "Docker SDK unavailable" error in logs

**Problem**: Cannot monitor Docker containers.

**Solution**: Ensure `/var/run/docker.sock` is mapped correctly with Read/Write access.

### Database resets after container restart

**Problem**: Tamagotchi loses level/XP on restart.

**Solution**: Map `/app/data` to a persistent host path like `/mnt/user/appdata/sysmon`.

### WebUI not loading

**Problem**: Cannot access `http://unraid-ip:8000`.

**Solution**: 
1. Check container is running: `docker ps | grep sysmon`
2. Check logs: `docker logs sysmon`
3. Verify port 8000 is not used by another container

---

## 🔒 Security Notes

- The container runs with `--pid=host` which gives it visibility into host processes
- Docker socket access (`/var/run/docker.sock`) is **read-only** (`:ro`) for security
- SysMon only **reads** system metrics, it does not modify anything
- No external internet access is required (except for initial image pull)

---

## 📱 Community Applications Template

If you want to add SysMon to Community Applications, here's the template:

```xml
<Container version="2">
  <Name>SysMon</Name>
  <Repository>peterpage2115/sysmon:latest</Repository>
  <Registry>https://hub.docker.com/r/peterpage2115/sysmon</Registry>
  <Network>bridge</Network>
  <Privileged>false</Privileged>
  <Support>https://github.com/PeterPage2115/SysMon/issues</Support>
  <Project>https://github.com/PeterPage2115/SysMon</Project>
  <Overview>Server Tamagotchi - Monitor your Unraid server through a cute creature that reflects system health</Overview>
  <Category>Tools:System</Category>
  <WebUI>http://[IP]:[PORT:8000]</WebUI>
  <Icon>https://raw.githubusercontent.com/PeterPage2115/SysMon/main/icon.png</Icon>
  <ExtraParams>--pid=host</ExtraParams>
  <PostArgs></PostArgs>
  <DonateText></DonateText>
  <DonateLink></DonateLink>
  <Description>
    SysMon is a gamified server monitoring tool that displays your Unraid server's health through a Tamagotchi-like creature. Feed it, level it up, and keep it happy by maintaining good server health!
  </Description>
  <Config Name="WebUI Port" Target="8000" Default="8000" Mode="tcp" Description="Web Interface Port" Type="Port" Display="always" Required="true" Mask="false">8000</Config>
  <Config Name="Docker Socket" Target="/var/run/docker.sock" Default="/var/run/docker.sock" Mode="rw" Description="Docker container monitoring" Type="Path" Display="always" Required="true" Mask="false">/var/run/docker.sock</Config>
  <Config Name="AppData" Target="/app/data" Default="/mnt/user/appdata/sysmon" Mode="rw" Description="Database persistence" Type="Path" Display="always" Required="true" Mask="false">/mnt/user/appdata/sysmon</Config>
</Container>
```

---

## 📚 Additional Resources

- **GitHub Repository**: https://github.com/PeterPage2115/SysMon
- **Docker Hub**: https://hub.docker.com/r/peterpage2115/sysmon
- **Issue Tracker**: https://github.com/PeterPage2115/SysMon/issues

---

## 🎮 Enjoy Your Server Tamagotchi!

Your server pet is now running! Keep it healthy by maintaining good server performance. Happy monitoring! 🖥️💚
