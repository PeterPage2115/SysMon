# Multi-stage build: 1) Build Svelte frontend, 2) Run Python backend
FROM node:20-alpine AS frontend-builder

WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build


# Python backend + serve static frontend
FROM python:3.11-slim

# Unraid metadata labels
LABEL net.unraid.docker.webui="http://[IP]:[PORT:8000]"
LABEL net.unraid.docker.icon="https://raw.githubusercontent.com/PeterPage2115/SysMon/main/icon.png"

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy VERSION file
COPY VERSION /app/VERSION

# Copy backend code
COPY backend/ .

# Copy built frontend from first stage
COPY --from=frontend-builder /frontend/dist /app/frontend/dist

# Create data directory for SQLite
RUN mkdir -p /app/data

# Expose port
EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
