import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec

JSON_FILE = "system_metrics.json"
INTERVAL = 5000  # milliseconds (5 seconds)

def read_metrics():
    try:
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def update_dashboard(i, axes):
    data = read_metrics()
    if not data:
        return

    times = [entry["timestamp"] for entry in data]
    cpu = [entry["cpu"] for entry in data]
    ram = [entry["ram"] for entry in data]
    disk = [entry["disk"] for entry in data]
    net_sent = [entry["net_sent"] for entry in data]
    net_recv = [entry["net_recv"] for entry in data]
    notepad = [entry["notepad_running"] for entry in data]

    # Clear all axes
    for ax in axes:
        ax.clear()

    # Plot CPU
    axes[0].plot(times, cpu, marker='o', color='orange')
    axes[0].set_title("CPU Usage (%)")
    axes[0].set_ylabel("CPU %")

    # Plot RAM
    axes[1].plot(times, ram, marker='o', color='green')
    axes[1].set_title("RAM Usage (%)")
    axes[1].set_ylabel("RAM %")

    # Plot Disk
    axes[2].plot(times, disk, marker='o', color='blue')
    axes[2].set_title("Disk Usage (%)")
    axes[2].set_ylabel("Disk %")

    # # Plot Network
    # axes[3].plot(times, net_sent, label='Sent MB', color='purple')
    # axes[3].plot(times, net_recv, label='Recv MB', color='red')
    # axes[3].set_title("Network I/O (MB)")
    # axes[3].set_ylabel("MB")
    # axes[3].legend()

    # Plot Notepad Availability
    axes[3].set_title("Notepad Availability")
    axes[3].plot(times, notepad, marker='o', color='black')
    axes[3].set_ylabel("Running (1) / Not (0)")
    axes[3].set_yticks([0, 1])
    axes[3].set_yticklabels(["No", "Yes"])

    # Shared x-label formatting
    for ax in axes:
        ax.set_xticks(times[::max(1, len(times)//8)])
        ax.set_xticklabels(times[::max(1, len(times)//8)], rotation=45)
        ax.set_xlabel("Time")
        ax.grid(True)

# Setup layout
fig = plt.figure(figsize=(12, 10))
gs = GridSpec(2, 2, figure=fig)
axes = [fig.add_subplot(gs[i, j]) for i in range(2) for j in range(2)]
# [(0,0), (0,1), (1,0), (1,1)]
print(axes)
fig.suptitle("📊 Live System Metrics Dashboard", fontsize=16)

ani = animation.FuncAnimation(fig, update_dashboard, fargs=(axes,), interval=INTERVAL)
plt.tight_layout()
plt.subplots_adjust(top=0.90)
plt.show()
