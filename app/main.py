import sys
import threading
import time
from shell.shell import start_shell
from engine.launcher import start_server

def main():
    # Start the Node.js server in a background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Give the server a moment to start up
    time.sleep(1)
    
    # Initialize and run the PyQt shell
    start_shell()

if __name__ == "__main__":
    main()