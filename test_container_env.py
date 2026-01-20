#!/usr/bin/env python3
"""Diagnostic script to test Docker environment in container."""
import os
import sys
from pathlib import Path

print("=" * 60)
print("CONTAINER ENVIRONMENT DIAGNOSTIC")
print("=" * 60)

# 1. Check Python version
print(f"\n1. Python: {sys.version}")

# 2. Check working directory
print(f"\n2. Working directory: {os.getcwd()}")

# 3. Check __file__ paths
print(f"\n3. Script location: {__file__}")
print(f"   Absolute: {Path(__file__).absolute()}")

# 4. Check VERSION file locations
print(f"\n4. VERSION file search:")
locations = [
    Path("/app/VERSION"),
    Path(__file__).parent / "VERSION",
    Path(__file__).parent.parent / "VERSION",
    Path(__file__).parent.parent.parent / "VERSION",
]
for loc in locations:
    exists = "✓" if loc.exists() else "✗"
    content = f" → {loc.read_text().strip()}" if loc.exists() else ""
    print(f"   {exists} {loc}{content}")

# 5. Check environment variables
print(f"\n5. Environment variables:")
docker_vars = ['DOCKER_HOST', 'DOCKER_TLS_VERIFY', 'DOCKER_CERT_PATH', 'DOCKER_API_VERSION']
for var in docker_vars:
    value = os.environ.get(var, 'NOT_SET')
    print(f"   {var}: {value}")

# 6. Check Docker socket
print(f"\n6. Docker socket:")
socket_path = Path("/var/run/docker.sock")
print(f"   Exists: {socket_path.exists()}")
if socket_path.exists():
    stat = socket_path.stat()
    print(f"   Permissions: {oct(stat.st_mode)}")
    print(f"   Owner: UID={stat.st_uid}, GID={stat.st_gid}")

# 7. Test Docker SDK
print(f"\n7. Docker SDK test:")
try:
    import docker
    print(f"   Docker SDK version: {docker.__version__}")
    
    # Test APIClient with correct URL scheme
    # Docker SDK expects 'http+unix://' prefix to mount UnixHTTPAdapter
    print(f"\n   Testing APIClient:")
    from docker import APIClient
    api_client = APIClient(
        base_url='http+unix:///var/run/docker.sock',
        version='1.41',  # Fixed version, no auto-detect
        timeout=10
    )
    version = api_client.version()
    print(f"   ✓ Connected - Docker v{version.get('Version')}, API v{version.get('ApiVersion')}")
    
    # List containers
    containers = api_client.containers(all=True)
    print(f"   ✓ Containers found: {len(containers)}")
    for c in containers[:3]:  # Show first 3
        print(f"      - {c.get('Names', [''])[0]} ({c.get('State')})")
    
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
