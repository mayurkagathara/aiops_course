import datetime # Module for working with dates and times.
import random   # Module for generating random numbers and choices.
import time     # Module for time-related functions, like delays.
import re       # Module for regular expressions.
import psutil   # Cross-platform library for system and process information.
import csv      # Module for reading and writing CSV files.
import json     # Module for working with JSON data.
import matplotlib.pyplot as plt # Matplotlib's plotting interface.
import seaborn as sns # High-level interface for drawing attractive statistical graphics.
import numpy as np # Numerical Python, for numerical operations (used for dummy data).

# --- Day 6: Simulating Log Files ---

LOG_LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]
INFO_MESSAGES = [
    "User '{user}' logged in from {ip}.",
    "Service '{service}' started successfully.",
    "Request to {endpoint} completed in {time_ms}ms."
]
ERROR_MESSAGES = [
    "Database connection failed: {error_code}.",
    "Service '{service}' crashed: {reason}.",
    "Disk space low on {disk_path}."
]

def generate_log_message(level: str) -> str:
    """
    Generates a random log message based on the specified level.

    Args:
        level (str): The log level (e.g., "INFO", "ERROR").

    Returns:
        str: A formatted log message.
    """
    if level == "INFO":
        user = random.choice(["alice", "bob", "charlie"]) # Selects a random user.
        ip = f"192.168.1.{random.randint(1, 254)}" # Generates a random IP last octet.
        service = random.choice(["auth-service", "data-api"]) # Selects a random service.
        endpoint = random.choice(["/users", "/data", "/status"]) # Selects a random endpoint.
        time_ms = random.randint(50, 500) # Generates random response time in ms.
        return random.choice(INFO_MESSAGES).format(user=user, ip=ip, service=service, endpoint=endpoint, time_ms=time_ms)
    elif level == "ERROR":
        service = random.choice(["auth-service", "data-api", "db-service"])
        error_code = random.choice(["CONN_REFUSED", "TIMEOUT", "AUTH_FAILED"])
        disk_path = random.choice(["/var/log", "/opt/app"])
        reason = random.choice(["Segmentation fault", "NullPointerException"])
        return random.choice(ERROR_MESSAGES).format(service=service, error_code=error_code, disk_path=disk_path, reason=reason)
    return "Generic log message."

def simulate_log_file(filename: str = "app.log", num_entries: int = 100, interval_seconds: float = 0.05):
    """
    Generates a simulated application log file with varying log levels and messages.

    Args:
        filename (str): The name of the log file to create.
        num_entries (int): The total number of log entries to generate.
        interval_seconds (float): Average time delay between generating entries in seconds.
    """
    current_time = datetime.datetime.now() # Gets the current datetime.
    print(f"Generating {num_entries} log entries to {filename}...")
    with open(filename, "w") as f: # Opens the file in write mode.
        for i in range(num_entries):
            # Skew log levels: INFO (70%), WARNING (20%), ERROR (8%), DEBUG (2%)
            level = random.choices(LOG_LEVELS, weights=[0.7, 0.2, 0.08, 0.02], k=1)[0]
            service = random.choice(["auth-service", "payment-service", "user-api", "inventory-db"])
            message = generate_log_message(level)
            
            # Format log line with milliseconds
            log_line = f"{current_time.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]} {level} [{service}] {message}\n"
            f.write(log_line) # Writes the formatted log line to the file.
            
            # Introduce slight variability in time intervals
            current_time += datetime.timedelta(seconds=random.uniform(interval_seconds * 0.5, interval_seconds * 1.5))
            
            # Small sleep to simulate real-time generation, avoid high CPU usage during simulation
            time.sleep(0.001) 

            if (i + 1) % 200 == 0: # Prints progress every 200 entries.
                print(f"  Generated {i + 1} entries...")

    print(f"Finished generating {num_entries} log entries to {filename}.")

# --- Day 7 (Part 1): Reading and Parsing Logs ---

def read_log_file(filepath: str) -> list[str]:
    """
    Reads a log file line by line, returning a list of stripped lines.

    Args:
        filepath (str): The path to the log file.

    Returns:
        list[str]: A list of log lines, with leading/trailing whitespace removed.
    """
    log_lines = []
    try:
        with open(filepath, 'r') as f: # Opens the file in read mode.
            for line in f: # Iterates over the file object line by line (memory efficient).
                log_lines.append(line.strip()) # Removes leading/trailing whitespace and newline.
        return log_lines
    except FileNotFoundError: # Catches error if file does not exist.
        print(f"Error: File not found at {filepath}")
        return []
    except Exception as e: # Catches any other exceptions during file reading.
        print(f"An error occurred while reading {filepath}: {e}")
        return []

def parse_basic_log(log_line: str) -> dict:
    """
    Parses a simple log line like 'LEVEL: Message' using string splitting.

    Args:
        log_line (str): The single log line string.

    Returns:
        dict: A dictionary with 'level' and 'message' keys.
    """
    parts = log_line.split(':', 1) # Splits the string by the first colon.
    if len(parts) == 2:
        return {"level": parts[0].strip().upper(), "message": parts[1].strip()}
    return {"level": "UNKNOWN", "message": log_line.strip()}

# Regex pattern for the simulated app.log format
# Example: 2023-10-26 10:05:30,123 INFO [auth-service] User 'alice' logged in from 192.168.1.100.
LOG_PATTERN = re.compile( # Compiles a regex pattern for efficiency.
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s+" # Captures timestamp.
    r"(?P<level>[A-Z]+)\s+\[(?P<service>.*?)\]\s+" # Captures level and service.
    r"(?P<message>.*)$" # Captures the rest as message.
)

def parse_complex_log(log_line: str) -> dict:
    """
    Parses a complex log line using a pre-compiled regular expression.

    Args:
        log_line (str): The single log line string.

    Returns:
        dict: A dictionary of captured groups (e.g., 'timestamp', 'level', 'service', 'message').
              Returns {'raw_line': ..., 'parse_error': ...} if no match.
    """
    match = LOG_PATTERN.search(log_line) # Searches for the pattern in the log line.
    if match:
        return match.groupdict() # Returns a dictionary of all named captured groups.
    return {"raw_line": log_line.strip(), "parse_error": "No match"}

# --- Day 7 (Part 2): Generating System Metrics (Intro) ---

def get_system_metrics() -> dict:
    """
    Collects basic system metrics using psutil.

    Returns:
        dict: A dictionary containing basic CPU, memory, disk, and network metrics.
    """
    cpu_percent = psutil.cpu_percent(interval=0.1) # Returns CPU usage percentage over 0.1 seconds.
    mem_info = psutil.virtual_memory() # Returns system memory usage statistics.
    disk_info = psutil.disk_usage('/') # Returns disk usage statistics for the root partition.
    net_io = psutil.net_io_counters() # Returns network I/O statistics.

    metrics = {
        "timestamp": datetime.datetime.now().isoformat(), # Current timestamp in ISO format.
        "cpu_percent": cpu_percent,
        "memory_percent": mem_info.percent, # Percentage of memory used.
        "memory_total_gb": round(mem_info.total / (1024**3), 2), # Total memory in GB.
        "memory_used_gb": round(mem_info.used / (1024**3), 2), # Used memory in GB.
        "disk_percent": disk_info.percent, # Percentage of disk used.
        "disk_total_gb": round(disk_info.total / (1024**3), 2), # Total disk space in GB.
        "disk_used_gb": round(disk_info.used / (1024**3), 2), # Used disk space in GB.
        "net_bytes_sent": net_io.bytes_sent, # Total bytes sent.
        "net_bytes_recv": net_io.bytes_recv # Total bytes received.
    }
    return metrics

# --- Day 8: Generating System Metrics (Deep Dive) & Storing Locally ---

def get_comprehensive_metrics() -> dict:
    """
    Collects a wider range of system metrics, including top processes.

    Returns:
        dict: A dictionary containing comprehensive system metrics.
    """
    metrics = {}
    metrics["timestamp"] = datetime.datetime.now().isoformat()

    # CPU metrics
    metrics["cpu_percent"] = psutil.cpu_percent(interval=None) # CPU usage since last call or boot.
    metrics["cpu_load_avg"] = [round(x, 2) for x in psutil.getloadavg()] # System load average (1, 5, 15 min).

    # Memory metrics
    mem = psutil.virtual_memory()
    metrics["mem_total_gb"] = round(mem.total / (1024**3), 2)
    metrics["mem_used_gb"] = round(mem.used / (1024**3), 2)
    metrics["mem_free_gb"] = round(mem.free / (1024**3), 2)
    metrics["mem_percent"] = mem.percent

    # Disk metrics
    disk_usage_root = psutil.disk_usage('/') # Disk usage for the root partition.
    metrics["disk_root_total_gb"] = round(disk_usage_root.total / (1024**3), 2)
    metrics["disk_root_used_gb"] = round(disk_usage_root.used / (1024**3), 2)
    metrics["disk_root_percent"] = disk_usage_root.percent
    metrics["disk_io_read_bytes"] = psutil.disk_io_counters().read_bytes # Total bytes read.
    metrics["disk_io_write_bytes"] = psutil.disk_io_counters().write_bytes # Total bytes written.

    # Network metrics
    net_io = psutil.net_io_counters()
    metrics["net_bytes_sent"] = net_io.bytes_sent
    metrics["net_bytes_recv"] = net_io.bytes_recv
    metrics["net_packets_sent"] = net_io.packets_sent # Total packets sent.
    metrics["net_packets_recv"] = net_io.packets_recv # Total packets received.

    # Processes (top 5 by CPU usage)
    metrics["top_processes_cpu"] = []
    # Iterates over all running processes and gets specific info.
    for proc in sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']), key=lambda p: p.info['cpu_percent'], reverse=True)[:5]:
        metrics["top_processes_cpu"].append({
            "pid": proc.info['pid'],
            "name": proc.info['name'],
            "cpu_percent": proc.info['cpu_percent'],
            "memory_percent": round(proc.info['memory_percent'], 2)
        })

    return metrics

def save_metrics_to_csv(metrics_list: list[dict], filename: str = "metrics.csv"):
    """
    Saves a list of metric dictionaries to a CSV file.

    Args:
        metrics_list (list[dict]): A list of dictionaries, where each dict is a set of metrics.
        filename (str): The name of the CSV file to create.
    """
    if not metrics_list:
        print("No metrics to save to CSV.")
        return

    # Dynamically get headers from the first dictionary's keys.
    # Flatten nested dictionaries for CSV compatibility if necessary (not done here for top_processes_cpu).
    fieldnames = []
    for key in metrics_list[0].keys():
        if key != "top_processes_cpu": # Exclude complex types not directly CSV compatible
            fieldnames.append(key)
    
    print(f"Saving metrics to {filename}...")
    with open(filename, 'w', newline='') as csvfile: # Opens file in write mode, newline='' prevents extra blank rows.
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames) # Creates a writer that maps dictionaries to CSV rows.
        writer.writeheader() # Writes the header row.
        
        # Write rows, excluding 'top_processes_cpu' which is a list of dicts
        for metrics_dict in metrics_list:
            row_to_write = {k: v for k, v in metrics_dict.items() if k in fieldnames}
            writer.writerow(row_to_write) # Writes a single row from a dictionary.
    print(f"Metrics saved to {filename}")

def save_data_to_json(data: list | dict, filename: str = "data.json"):
    """
    Saves data (list of dicts or a single dict) to a JSON file.

    Args:
        data (list | dict): The data to save.
        filename (str): The name of the JSON file to create.
    """
    print(f"Saving data to {filename}...")
    with open(filename, 'w') as jsonfile: # Opens the file in write mode.
        json.dump(data, jsonfile, indent=4) # Serializes data to JSON and writes to file, with 4-space indentation.
    print(f"Data saved to {filename}")

def load_data_from_json(filename: str = "data.json") -> list | dict | None:
    """
    Loads data from a JSON file.

    Args:
        filename (str): The name of the JSON file to load.

    Returns:
        list | dict | None: The loaded data, or None if an error occurs.
    """
    try:
        with open(filename, 'r') as jsonfile: # Opens the file in read mode.
            data = json.load(jsonfile) # Deserializes JSON data from file.
        print(f"Data loaded from {filename}")
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {filename}")
        return None
    except json.JSONDecodeError as e: # Catches error if JSON is malformed.
        print(f"Error decoding JSON from {filename}: {e}")
        return None

# --- Day 10: Visualizing Data ---

def generate_dummy_cpu_data(num_points: int = 60) -> tuple[list[datetime.datetime], list[float]]:
    """
    Generates dummy CPU usage data over a period.

    Args:
        num_points (int): Number of data points to generate.

    Returns:
        tuple[list[datetime.datetime], list[float]]: Timestamps and corresponding CPU values.
    """
    timestamps = []
    cpu_values = []
    current_time = datetime.datetime.now() # Gets current time.
    for i in range(num_points):
        timestamps.append(current_time)
        # Simulate some fluctuating CPU usage with a slight upward trend
        cpu_values.append(random.uniform(20, 80) + (5 * (i / num_points)))
        current_time += datetime.timedelta(minutes=1) # Increments time by 1 minute.
    return timestamps, cpu_values

def plot_cpu_trend(timestamps: list[datetime.datetime], cpu_values: list[float]):
    """
    Plots a simulated CPU usage trend over time using Matplotlib.

    Args:
        timestamps (list[datetime.datetime]): List of datetime objects for the x-axis.
        cpu_values (list[float]): List of CPU usage percentages for the y-axis.
    """
    plt.figure(figsize=(10, 6)) # Creates a new figure and axes.
    plt.plot(timestamps, cpu_values, marker='o', linestyle='-', color='#004777', markersize=4) # Plots the data.
    plt.title('Simulated CPU Usage Trend Over Time', fontsize=16, color='#004777') # Sets plot title.
    plt.xlabel('Time', fontsize=12, color='#004777') # Sets x-axis label.
    plt.ylabel('CPU Usage (%)', fontsize=12, color='#004777') # Sets y-axis label.
    plt.grid(True, linestyle='--', alpha=0.7) # Adds a grid to the plot.
    plt.ylim(0, 100) # Sets y-axis limits.
    plt.xticks(rotation=45, ha='right') # Rotates x-axis labels for readability.
    plt.tight_layout() # Adjusts plot parameters for a tight layout.
    # plt.show() # Uncomment to display the plot (will block execution).

def plot_latency_distribution(data: np.ndarray):
    """
    Plots the distribution of hypothetical API latency using Seaborn.

    Args:
        data (np.ndarray): Numerical data representing latency values.
    """
    plt.figure(figsize=(8, 5))
    sns.histplot(data, kde=True, color='#00AFB9', bins=30) # Creates a histogram with a Kernel Density Estimate.
    plt.title('Distribution of API Latency', fontsize=16, color='#004777')
    plt.xlabel('Latency (ms)', fontsize=12, color='#004777')
    plt.ylabel('Frequency', fontsize=12, color='#004777')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    # plt.show() # Uncomment to display the plot (will block execution).

# --- Main Execution Block for Demonstrations ---
if __name__ == "__main__":
    print("--- AIOps Week 2 Python Code Reference ---")
    print("\n--- Day 6: Simulating Log Files ---")
    simulate_log_file(num_entries=500, interval_seconds=0.01)

    print("\n--- Day 7 (Part 1): Reading and Parsing Logs ---")
    log_file_path = "app.log"
    raw_logs = read_log_file(log_file_path)
    if raw_logs:
        print(f"First raw log entry: {raw_logs[0]}")
        
        print("\n  Parsing basic log (string split):")
        basic_parsed = parse_basic_log("INFO: User logged in.")
        print(basic_parsed)
        
        print("\n  Parsing complex log (regex):")
        complex_parsed = parse_complex_log(raw_logs[0])
        print(complex_parsed)
    else:
        print("No logs to parse. Ensure 'app.log' was generated.")

    print("\n--- Day 7 (Part 2): Generating System Metrics (Intro) ---")
    print("  Collecting basic system metrics (snapshot):")
    basic_metrics_snapshot = get_system_metrics()
    print(basic_metrics_snapshot)

    print("\n--- Day 8: Generating System Metrics (Deep Dive) & Storing Locally ---")
    print("  Collecting comprehensive metrics (snapshot):")
    comp_metrics_snapshot = get_comprehensive_metrics()
    print(comp_metrics_snapshot)

    # Simulate collecting multiple comprehensive metrics for storage
    print("\n  Simulating collection of 3 comprehensive metrics for storage...")
    collected_comp_metrics = []
    for _ in range(3):
        collected_comp_metrics.append(get_comprehensive_metrics())
        time.sleep(0.5) # Small delay for distinct timestamps

    print("\n  Saving comprehensive metrics to CSV (excluding complex types)...")
    save_metrics_to_csv(collected_comp_metrics, "comprehensive_metrics_simple.csv")

    print("\n  Saving comprehensive metrics to JSON...")
    save_data_to_json(collected_comp_metrics, "comprehensive_metrics.json")
    
    print("\n  Loading comprehensive metrics from JSON...")
    loaded_json_data = load_data_from_json("comprehensive_metrics.json")
    if loaded_json_data:
        print(f"  First loaded entry from JSON: {loaded_json_data[0]}")

    print("\n--- Day 10: Visualizing Data ---")
    print("  Generating dummy CPU data and preparing plot...")
    timestamps, cpu_values = generate_dummy_cpu_data(num_points=30)
    plot_cpu_trend(timestamps, cpu_values)
    print("  CPU trend plot prepared. Uncomment 'plt.show()' in function to display.")

    print("\n  Generating dummy latency data and preparing plot...")
    latency_data = np.random.normal(loc=150, scale=30, size=500)
    latency_data = latency_data[latency_data > 0] # Ensure no negative latency
    plot_latency_distribution(latency_data)
    print("  Latency distribution plot prepared. Uncomment 'plt.show()' in function to display.")

    print("\n--- End of AIOps Week 2 Python Reference ---")
    print("Note: For plots to display, you need to uncomment 'plt.show()' calls in the respective functions and run this script in an environment that supports GUI rendering (e.g., local Python interpreter).")
