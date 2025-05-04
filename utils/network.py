import requests
import os

API = os.getenv("URL")

def is_connected():
    try:
        requests.get(f"{API}/api/historial/connect", timeout=3)
        return True
    except requests.RequestException:
        return False