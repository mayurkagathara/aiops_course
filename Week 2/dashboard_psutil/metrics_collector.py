import psutil
import json
import time
from datetime import datetime

# File to store the collected metrics
JSON_FILE = "system_metrics.json"
INTERVAL = 5  # seconds
MAX_ENTRIES = 100  # store only the latest 100 entries

def is_process_running(name):
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() == name.lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

metrics = []

print(f"[Collector] Starting to collect metrics every {INTERVAL} seconds...")
while True:
    now = datetime.now().strftime("%H:%M:%S")
    data = {
        "timestamp": now,
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "net_sent": psutil.net_io_counters().bytes_sent / (1024 * 1024),   # in MB
        "net_recv": psutil.net_io_counters().bytes_recv / (1024 * 1024),   # in MB
        "notepad_running": int(is_process_running("notepad.exe"))
    }

    metrics.append(data)
    metrics = metrics[-MAX_ENTRIES:]  # keep only latest entries

    with open(JSON_FILE, "w") as f:
        json.dump(metrics, f, indent=2)

    time.sleep(INTERVAL)
