#!/usr/bin/env python3
"""
Check if all dependencies are installed and configured correctly.
"""
import sys
import subprocess

def check_python_package(package_name, import_name=None):
    """Check if a Python package is installed."""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✓ {package_name} is installed")
        return True
    except ImportError:
        print(f"✗ {package_name} is NOT installed")
        return False

def check_system_command(command, name=None):
    """Check if a system command is available."""
    if name is None:
        name = command
    
    try:
        result = subprocess.run(
            [command, "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✓ {name} is installed")
            return True
        else:
            print(f"✗ {name} is NOT installed or not working")
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print(f"✗ {name} is NOT installed")
        return False

def check_redis_connection():
    """Check if Redis is accessible."""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0, socket_connect_timeout=2)
        r.ping()
        print(f"✓ Redis is running and accessible")
        return True
    except Exception as e:
        print(f"✗ Redis is NOT accessible: {e}")
        return False

def main():
    print("Checking CineScale Setup...")
    print("=" * 60)
    
    all_ok = True
    
    # Check Python packages
    print("\nPython Dependencies:")
    packages = [
        ("celery", "celery"),
        ("redis", "redis"),
        ("fastapi", "fastapi"),
        ("pydantic", "pydantic"),
    ]
    
    for pkg, imp in packages:
        if not check_python_package(pkg, imp):
            all_ok = False
    
    # Check system commands
    print("\nSystem Dependencies:")
    if not check_system_command("ffmpeg"):
        all_ok = False
    if not check_system_command("ffprobe"):
        all_ok = False
    
    # Check Redis
    print("\nServices:")
    if not check_redis_connection():
        all_ok = False
    
    print("\n" + "=" * 60)
    if all_ok:
        print("✓ All checks passed! You're ready to go.")
        print("\nNext steps:")
        print("  1. Start worker: start_worker.bat")
        print("  2. Submit test job: python test_worker.py")
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        print("\nTo install Python dependencies:")
        print("  pip install -r requirements.txt")
        print("\nTo start Redis:")
        print("  docker-compose up redis")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
