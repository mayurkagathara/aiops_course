import psutil
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import os

# -----------------------
# Configuration
# -----------------------

MONITOR_DURATION = 60  # seconds
INTERVAL = 5  # seconds between updates
PROCESS_NAME = "notepad.exe"  # Example process for availability check

# Store data points
timestamps = []
cpu_usages = []
ram_usages = []
disk_usages = []
net_sent = []
net_recv = []
process_status = []  # 1 = running, 0 = not running

# Helper to check if a process is running
def is_process_running(name):
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() == name.lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

# -----------------------
# Collecting Metrics
# -----------------------

print(f"Monitoring system metrics every {INTERVAL}s for {MONITOR_DURATION}s...")
start_time = time.time()
while time.time() - start_time < MONITOR_DURATION:
    timestamps.append(time.strftime("%H:%M:%S"))

    cpu_usages.append(psutil.cpu_percent())
    ram_usages.append(psutil.virtual_memory().percent)
    disk_usages.append(psutil.disk_usage('/').percent)
    net_io = psutil.net_io_counters()
    net_sent.append(net_io.bytes_sent / (1024 * 1024))  # Convert to MB
    net_recv.append(net_io.bytes_recv / (1024 * 1024))  # Convert to MB

    # Check if process is running (1 = running, 0 = not running)
    process_status.append(1 if is_process_running(PROCESS_NAME) else 0)

    time.sleep(INTERVAL)

print("✅ Data collection complete.")

# -----------------------
# Plotting with Matplotlib
# -----------------------

def plot_cpu_usage():
    plt.figure(figsize=(8, 4))
    plt.plot(timestamps, cpu_usages, marker='o', color='orange')
    plt.title("CPU Usage Over Time")
    plt.xlabel("Time")
    plt.ylabel("CPU %")
    plt.xticks(rotation=45)
    plt.tight_layout()

# -----------------------
# Plotting with Seaborn
# -----------------------

def plot_ram_usage():
    plt.figure(figsize=(8, 4))
    sns.lineplot(x=timestamps, y=ram_usages, marker='o', color='green')
    plt.title("RAM Usage Over Time")
    plt.xlabel("Time")
    plt.ylabel("RAM %")
    plt.xticks(rotation=45)
    plt.tight_layout()

# -----------------------
# Plotting with Plotly
# -----------------------

def plot_disk_network_usage():
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Disk Usage", "Network I/O"))

    fig.add_trace(go.Scatter(x=timestamps, y=disk_usages, mode='lines+markers',
                             name="Disk %", line=dict(color='blue')), row=1, col=1)

    fig.add_trace(go.Scatter(x=timestamps, y=net_sent, mode='lines+markers',
                             name="Net Sent (MB)", line=dict(color='purple')), row=1, col=2)

    fig.add_trace(go.Scatter(x=timestamps, y=net_recv, mode='lines+markers',
                             name="Net Received (MB)", line=dict(color='red')), row=1, col=2)

    fig.update_layout(height=400, width=1000, title_text="Disk and Network Metrics")
    fig.show()

# -----------------------
# Process availability chart
# -----------------------

def plot_process_availability():
    plt.figure(figsize=(8, 4))
    plt.plot(timestamps, process_status, marker='o', linestyle='-', color='red')
    plt.title(f"Availability of '{PROCESS_NAME}'")
    plt.xlabel("Time")
    plt.ylabel("Status (1=Running, 0=Stopped)")
    plt.yticks([0, 1], ["Stopped", "Running"])
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

# -----------------------
# Show Dashboard
# -----------------------

def show_dashboard():
    print("📊 Displaying charts...")

    # Use matplotlib for CPU and process availability
    plt.figure(figsize=(10, 8))

    plt.subplot(2, 1, 1)
    plt.plot(timestamps, cpu_usages, marker='o', color='orange', label="CPU Usage")
    plt.ylabel("CPU %")
    plt.xticks(rotation=45)
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(timestamps, process_status, marker='o', color='red', label=f"{PROCESS_NAME} Status")
    plt.xlabel("Time")
    plt.ylabel("Availability")
    plt.yticks([0, 1], ["Stopped", "Running"])
    plt.xticks(rotation=45)
    plt.legend()

    plt.suptitle("CPU Usage and Process Availability (Matplotlib)", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

    # Seaborn for RAM
    plot_ram_usage()
    plt.show()

    # Plotly for disk + network
    plot_disk_network_usage()

# -----------------------
# Run
# -----------------------

if __name__ == "__main__":
    show_dashboard()