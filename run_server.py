from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import socket
import os

app = FastAPI()

# Serve the current folder as the website
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount(
    "/",
    StaticFiles(directory=BASE_DIR, html=True),
    name="static"
)


def get_local_ip():
    """Get the computer's LAN IPv4 address."""
    try:
        # Doesn't actually send data; determines the preferred network interface.
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except Exception:
        return "127.0.0.1"


if __name__ == "__main__":
    ip = get_local_ip()

    print()
    print("Server running at:")
    print("  Local:   http://127.0.0.1:8000")
    print(f"  Network: http://{ip}:8000")
    print()

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )