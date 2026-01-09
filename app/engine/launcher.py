import subprocess
import os
import sys

def get_frontend_path():
    """Get the absolute path to frontend server.js"""
    engine_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.dirname(engine_dir)
    server_path = os.path.join(app_dir, 'frontend', 'server.js')
    return server_path

def get_backend_path():
    """Get the absolute path to FastAPI server"""
    engine_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.dirname(engine_dir)
    root_dir = os.path.dirname(app_dir)
    server_path = os.path.join(root_dir, 'server', 'main.py')
    return server_path

def start_frontend():
    """Start the Node.js frontend server"""
    server_path = get_frontend_path()
    
    if not os.path.exists(server_path):
        print(f"Error: server.js not found at {server_path}")
        return None
    
    print(f"Starting frontend server from: {server_path}")
    
    try:
        process = subprocess.Popen(
            ['node', server_path],
            cwd=os.path.dirname(server_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process
    except FileNotFoundError:
        print("Error: Node.js is not installed or not in PATH")
        return None
    except Exception as e:
        print(f"Error starting frontend server: {e}")
        return None

def start_backend():
    """Start the FastAPI backend server"""
    server_path = get_backend_path()
    server_dir = os.path.dirname(server_path)
    
    if not os.path.exists(server_path):
        print(f"Error: main.py not found at {server_path}")
        return None
    
    print(f"Starting backend server from: {server_path}")
    
    try:
        process = subprocess.Popen(
            [sys.executable, '-m', 'uvicorn', 'main:app', '--host', '0.0.0.0', '--port', '8000', '--reload'],
            cwd=server_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process
    except Exception as e:
        print(f"Error starting backend server: {e}")
        return None

def start_servers():
    """Start both frontend and backend servers"""
    frontend_process = start_frontend()
    backend_process = start_backend()
    
    return frontend_process, backend_process

if __name__ == "__main__":
    frontend, backend = start_servers()
    
    if frontend:
        print("Frontend server started on http://localhost:3000")
    if backend:
        print("Backend API started on http://localhost:8000")
    
    # Keep running
    try:
        if frontend:
            frontend.wait()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        if frontend:
            frontend.terminate()
        if backend:
            backend.terminate()
