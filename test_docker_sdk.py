"""Quick test script to verify Docker SDK connection."""
import docker

print("Testing Docker SDK connection...")
print()

# Test 1: from_env()
print("1. Testing docker.from_env():")
try:
    client = docker.from_env()
    print(f"   ✓ Connected: {client.ping()}")
    print(f"   ✓ Version: {client.version()['Version']}")
except Exception as e:
    print(f"   ✗ Failed: {e}")

print()

# Test 2: DockerClient with unix:// (2 slashes)
print("2. Testing DockerClient(base_url='unix://var/run/docker.sock'):")
try:
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    print(f"   ✓ Connected: {client.ping()}")
    print(f"   ✓ Version: {client.version()['Version']}")
except Exception as e:
    print(f"   ✗ Failed: {e}")

print()

# Test 3: DockerClient with unix:/// (3 slashes)
print("3. Testing DockerClient(base_url='unix:///var/run/docker.sock'):")
try:
    client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
    print(f"   ✓ Connected: {client.ping()}")
    print(f"   ✓ Version: {client.version()['Version']}")
    
    # Test listing containers
    containers = client.containers.list()
    print(f"   ✓ Found {len(containers)} running containers")
except Exception as e:
    print(f"   ✗ Failed: {e}")

print()
print("Test complete!")
