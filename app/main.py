import sys
import time
import subprocess
import os
import urllib.request
from shell.shell import start_shell

def get_frontend_path():
    """Get the absolute path to frontend server.js"""
    app_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(app_dir, 'frontend', 'server.js')
    return server_path

def start_frontend():
    """Start the Node.js frontend server"""
    server_path = get_frontend_path()
    frontend_dir = os.path.dirname(server_path)
    
    if not os.path.exists(server_path):
        print(f"Error: server.js not found at {server_path}")
        return None
    
    # Check if node_modules exists, if not run npm install
    node_modules = os.path.join(frontend_dir, 'node_modules')
    if not os.path.exists(node_modules):
        print("Installing frontend dependencies...")
        subprocess.run(['npm', 'install'], cwd=frontend_dir, shell=True)
    
    print("Starting frontend server...")
    
    try:
        process = subprocess.Popen(
            ['node', server_path],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Wait a moment and check for immediate errors
        time.sleep(2)
        
        if process.poll() is not None:
            # Process ended, read output for error
            output = process.stdout.read()
            print(f"Server error: {output}")
            return None
        
        return process
    except FileNotFoundError:
        print("Error: Node.js is not installed or not in PATH")
        return None
    except Exception as e:
        print(f"Error starting frontend server: {e}")
        return None

def check_server(url, name, retries=5):
    """Check if a server is running at the given URL"""
    for i in range(retries):
        try:
            urllib.request.urlopen(url, timeout=2)
            print(f"✓ {name} is running at {url}")
            return True
        except Exception:
            if i < retries - 1:
                time.sleep(0.5)
    print(f"✗ {name} not available at {url}")
    return False

def main():
    # Start frontend server
    frontend_process = start_frontend()
    
    if not frontend_process:
        print("Failed to start frontend server")
        sys.exit(1)
    
    # Wait for frontend to be ready
    frontend_ok = check_server("http://localhost:3000", "Frontend server")
    
    if not frontend_ok:
        print("Frontend server failed to start")
        # Try to get error output
        if frontend_process.poll() is None:
            frontend_process.terminate()
        sys.exit(1)
    
    # Check backend API (don't start it, just check)
    backend_ok = check_server("http://localhost:8000/health", "Backend API")
    
    if not backend_ok:
        print("\nNote: Backend API not running. Auth features won't work.")
        print("  To start: cd server && uvicorn main:app --reload")
    
    print("\nLaunching Seyyul...")
    
    try:
        start_shell()
    finally:
        # Clean up frontend server when shell closes
        if frontend_process and frontend_process.poll() is None:
            frontend_process.terminate()
            print("Frontend server stopped")

if __name__ == "__main__":
    main()