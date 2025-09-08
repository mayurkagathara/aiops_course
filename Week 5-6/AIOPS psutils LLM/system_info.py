
import psutil
import platform
import time
import socket

def collect_system_data():
    return {
        "platform": platform.system(),
        "platform-release": platform.release(),
        "hostname": socket.gethostname(),
        "boot_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(psutil.boot_time())),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
        "virtual_memory": psutil.virtual_memory()._asdict(),
        "swap_memory": psutil.swap_memory()._asdict(),
        "disk_usage": {part.mountpoint: psutil.disk_usage(part.mountpoint)._asdict()
                       for part in psutil.disk_partitions()},
        "disk_io": psutil.disk_io_counters()._asdict(),
        "net_io": psutil.net_io_counters()._asdict(),
        "process_count": len(psutil.pids())
    }
