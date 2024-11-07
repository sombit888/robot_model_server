import http.server
import socketserver
import subprocess
import time
import sys
import os

# Configuration
PORT = 8000  # Port for the Python HTTP server
DIRECTORY = "/home/sombit_dey/vision_code/hosting/test"  # Directory containing the website files

# Create a directory and an index.html file if not exists
os.makedirs(DIRECTORY, exist_ok=True)
with open(f"{DIRECTORY}/index.html", "w") as f:
    f.write("<html><body><h1>Welcome to My Dummy Website!</h1></body></html>")

# Start the Python HTTP server in a separate thread
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

# Run HTTP server in a new process
server_process = subprocess.Popen([
    sys.executable, "-m", "http.server", str(PORT), "--directory", DIRECTORY
])

# Give the server a moment to start
time.sleep(2)

# Start ngrok
try:
    print("Starting ngrok...")
    ngrok_process = subprocess.Popen(["/home/sombit_dey/ngrok", "http", str(PORT)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)  # Give ngrok time to initialize

    # Parse the public URL from ngrok's output
    output = subprocess.check_output(["curl", "-s", "http://localhost:4040/api/tunnels"])
    import json
    tunnels = json.loads(output)
    public_url = tunnels['tunnels'][0]['public_url']
    print(f"Public URL: {public_url}")

    print("\nYour website is accessible at:", public_url)
    print("Press Ctrl+C to terminate.")
    
    # Keep the script running until interrupted
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nShutting down...")
finally:
    server_process.terminate()
    ngrok_process.terminate()
