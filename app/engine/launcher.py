import subprocess
import os
import sys

def get_server_path():
    """Get the absolute path to server.js"""
    # Get the directory where this script is located
    engine_dir = os.path.dirname(os.path.abspath(__file__))
    # Navigate to frontend directory (sibling of engine)
    app_dir = os.path.dirname(engine_dir)
    server_path = os.path.join(app_dir, 'frontend', 'server.js')
    return server_path

def start_server():
    """Start the Node.js server"""
    server_path = get_server_path()
    
    if not os.path.exists(server_path):
        print(f"Error: server.js not found at {server_path}")
        sys.exit(1)
    
    print(f"Starting server from: {server_path}")
    
    try:
        # Start the Node.js server
        # Using shell=True on Windows for proper command execution
        process = subprocess.Popen(
            ['node', server_path],
            cwd=os.path.dirname(server_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Stream the output
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        # Check for any errors
        stderr = process.stderr.read()
        if stderr:
            print(f"Server Error: {stderr}", file=sys.stderr)
            
        return process.returncode
        
    except FileNotFoundError:
        print("Error: Node.js is not installed or not in PATH")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_server()
