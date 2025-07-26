import streamlit as st # Streamlit library for creating web applications.
import datetime # Module for working with dates and times.
import random   # Module for generating random numbers and choices.
import time     # Module for time-related functions, like delays.
import re       # Module for regular expressions.
import psutil   # Cross-platform library for system and process information.
import csv      # Module for reading and writing CSV files.
import json     # Module for working with JSON data.
import matplotlib.pyplot as plt # Matplotlib's plotting interface.
import seaborn as sns # High-level interface for drawing attractive statistical graphics.
import numpy as np # Numerical Python, for numerical operations.
import pandas as pd # Data analysis and manipulation library (useful for display).

# --- Consolidated Functions from aiops-week2-python-reference ---
# These functions are embedded directly into this Streamlit app for self-containment.

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
    """
    if level == "INFO":
        user = random.choice(["alice", "bob", "charlie"])
        ip = f"192.168.1.{random.randint(1, 254)}"
        service = random.choice(["auth-service", "data-api"])
        endpoint = random.choice(["/users", "/data", "/status"])
        time_ms = random.randint(50, 500)
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
    """
    current_time = datetime.datetime.now()
    status_placeholder = st.empty() # Placeholder for real-time updates in Streamlit.
    status_placeholder.info(f"Generating {num_entries} log entries to {filename}...")
    
    with open(filename, "w") as f:
        for i in range(num_entries):
            level = random.choices(LOG_LEVELS, weights=[0.7, 0.2, 0.08, 0.02], k=1)[0]
            service = random.choice(["auth-service", "payment-service", "user-api", "inventory-db"])
            message = generate_log_message(level)
            
            log_line = f"{current_time.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]} {level} [{service}] {message}\n"
            f.write(log_line)
            
            current_time += datetime.timedelta(seconds=random.uniform(interval_seconds * 0.5, interval_seconds * 1.5))
            time.sleep(0.001) 

            if (i + 1) % 100 == 0:
                status_placeholder.info(f"Generated {i + 1} entries...")

    status_placeholder.success(f"Finished generating {num_entries} log entries to {filename}.")

# --- Day 7 (Part 1): Reading and Parsing Logs ---
def read_log_file(filepath: str) -> list[str]:
    """
    Reads a log file line by line, returning a list of stripped lines.
    """
    log_lines = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                log_lines.append(line.strip())
        return log_lines
    except FileNotFoundError:
        st.error(f"Error: File not found at {filepath}")
        return []
    except Exception as e:
        st.error(f"An error occurred while reading {filepath}: {e}")
        return []

def parse_basic_log(log_line: str) -> dict:
    """
    Parses a simple log line like 'LEVEL: Message' using string splitting.
    """
    parts = log_line.split(':', 1)
    if len(parts) == 2:
        return {"level": parts[0].strip().upper(), "message": parts[1].strip()}
    return {"level": "UNKNOWN", "message": log_line.strip()}

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s+"
    r"(?P<level>[A-Z]+)\s+\[(?P<service>.*?)\]\s+"
    r"(?P<message>.*)$"
)

def parse_complex_log(log_line: str) -> dict:
    """
    Parses a complex log line using a pre-compiled regular expression.
    """
    match = LOG_PATTERN.search(log_line)
    if match:
        return match.groupdict()
    return {"raw_line": log_line.strip(), "parse_error": "No match"}

# --- Day 7 (Part 2): Generating System Metrics (Intro) ---
def get_system_metrics() -> dict:
    """
    Collects basic system metrics using psutil.
    """
    cpu_percent = psutil.cpu_percent(interval=0.1)
    mem_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')
    net_io = psutil.net_io_counters()

    metrics = {
        "timestamp": datetime.datetime.now().isoformat(),
        "cpu_percent": cpu_percent,
        "memory_percent": mem_info.percent,
        "memory_total_gb": round(mem_info.total / (1024**3), 2),
        "memory_used_gb": round(mem_info.used / (1024**3), 2),
        "disk_percent": disk_info.percent,
        "disk_total_gb": round(disk_info.total / (1024**3), 2),
        "disk_used_gb": round(disk_info.used / (1024**3), 2),
        "net_bytes_sent": net_io.bytes_sent,
        "net_bytes_recv": net_io.bytes_recv
    }
    return metrics

# --- Day 8: Generating System Metrics (Deep Dive) & Storing Locally ---
def get_comprehensive_metrics() -> dict:
    """
    Collects a wider range of system metrics, including top processes.
    """
    metrics = {}
    metrics["timestamp"] = datetime.datetime.now().isoformat()

    metrics["cpu_percent"] = psutil.cpu_percent(interval=None)
    metrics["cpu_load_avg"] = [round(x, 2) for x in psutil.getloadavg()]

    mem = psutil.virtual_memory()
    metrics["mem_total_gb"] = round(mem.total / (1024**3), 2)
    metrics["mem_used_gb"] = round(mem.used / (1024**3), 2)
    metrics["mem_free_gb"] = round(mem.free / (1024**3), 2)
    metrics["mem_percent"] = mem.percent

    disk_usage_root = psutil.disk_usage('/')
    metrics["disk_root_total_gb"] = round(disk_usage_root.total / (1024**3), 2)
    metrics["disk_root_used_gb"] = round(disk_usage_root.used / (1024**3), 2)
    metrics["disk_root_percent"] = disk_usage_root.percent
    metrics["disk_io_read_bytes"] = psutil.disk_io_counters().read_bytes
    metrics["disk_io_write_bytes"] = psutil.disk_io_counters().write_bytes

    net_io = psutil.net_io_counters()
    metrics["net_bytes_sent"] = net_io.bytes_sent
    metrics["net_bytes_recv"] = net_io.bytes_recv
    metrics["net_packets_sent"] = net_io.packets_sent
    metrics["net_packets_recv"] = net_io.packets_recv

    metrics["top_processes_cpu"] = []
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
    """
    if not metrics_list:
        st.warning("No metrics to save to CSV.")
        return

    fieldnames = []
    for key in metrics_list[0].keys():
        if key != "top_processes_cpu":
            fieldnames.append(key)
    
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for metrics_dict in metrics_list:
                row_to_write = {k: v for k, v in metrics_dict.items() if k in fieldnames}
                writer.writerow(row_to_write)
        st.success(f"Metrics saved to {filename}")
    except Exception as e:
        st.error(f"Error saving to CSV: {e}")

def save_data_to_json(data: list | dict, filename: str = "data.json"):
    """
    Saves data (list of dicts or a single dict) to a JSON file.
    """
    try:
        with open(filename, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=4)
        st.success(f"Data saved to {filename}")
    except Exception as e:
        st.error(f"Error saving to JSON: {e}")

def load_data_from_json(filename: str = "data.json") -> list | dict | None:
    """
    Loads data from a JSON file.
    """
    try:
        with open(filename, 'r') as jsonfile:
            data = json.load(jsonfile)
        st.success(f"Data loaded from {filename}")
        return data
    except FileNotFoundError:
        st.error(f"Error: File not found at {filename}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON from {filename}: {e}")
        return None

# --- Day 10: Visualizing Data ---
def generate_dummy_cpu_data(num_points: int = 60) -> tuple[list[datetime.datetime], list[float]]:
    """
    Generates dummy CPU usage data over a period.
    """
    timestamps = []
    cpu_values = []
    current_time = datetime.datetime.now()
    for i in range(num_points):
        timestamps.append(current_time)
        cpu_values.append(random.uniform(20, 80) + (5 * (i / num_points)))
        current_time += datetime.timedelta(minutes=1)
    return timestamps, cpu_values

def plot_cpu_trend(timestamps: list[datetime.datetime], cpu_values: list[float]) -> plt.Figure:
    """
    Plots a simulated CPU usage trend over time using Matplotlib.
    Returns the Matplotlib figure object.
    """
    fig, ax = plt.subplots(figsize=(10, 6)) # Creates a figure and a set of subplots.
    ax.plot(timestamps, cpu_values, marker='o', linestyle='-', color='#004777', markersize=4)
    ax.set_title('Simulated CPU Usage Trend Over Time', fontsize=16, color='#004777')
    ax.set_xlabel('Time', fontsize=12, color='#004777')
    ax.set_ylabel('CPU Usage (%)', fontsize=12, color='#004777')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_ylim(0, 100)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig # Returns the figure object.

def plot_latency_distribution(data: np.ndarray) -> plt.Figure:
    """
    Plots the distribution of hypothetical API latency using Seaborn.
    Returns the Matplotlib figure object.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(data, kde=True, color='#00AFB9', bins=30, ax=ax) # Passes the axes object to seaborn.
    ax.set_title('Distribution of API Latency', fontsize=16, color='#004777')
    ax.set_xlabel('Latency (ms)', fontsize=12, color='#004777')
    ax.set_ylabel('Frequency', fontsize=12, color='#004777')
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    return fig # Returns the figure object.

# --- Streamlit Application Layout ---

st.set_page_config(layout="wide", page_title="AIOps Week 2 Playground")

st.title("AIOps Week 2: Practical Playground")
st.markdown("Explore and interact with core AIOps concepts: log simulation, parsing, metric collection, data storage, and visualization.")

# --- Day 6: Simulating Log Files ---
st.header("1. Log File Simulation (Day 6)")
st.write("Generate a simulated application log file with various log levels and messages.")
log_filename = st.text_input("Log File Name:", "app.log", key="log_file_name_input")
num_log_entries = st.number_input("Number of Log Entries:", min_value=10, max_value=10000, value=500, step=100, key="num_log_entries_input")
log_interval = st.slider("Average Interval Between Entries (seconds):", min_value=0.001, max_value=0.1, value=0.01, step=0.001, format="%.3f", key="log_interval_slider")

if st.button("Generate Logs", key="generate_logs_button"):
    simulate_log_file(log_filename, num_log_entries, log_interval)

# --- Day 7 (Part 1): Reading and Parsing Logs ---
st.header("2. Reading & Parsing Logs (Day 7.1)")
st.write("Read and parse log entries from a file.")
read_log_filepath = st.text_input("File to Read:", "app.log", key="read_log_filepath_input")

if st.button("Read Logs", key="read_logs_button"):
    raw_logs = read_log_file(read_log_filepath)
    if raw_logs:
        st.subheader("Raw Log Entries (First 10)")
        for i, log_line in enumerate(raw_logs[:10]):
            st.code(log_line)
        
        st.subheader("Parse Log Entries")
        parse_type = st.radio("Choose Parsing Method:", ("Basic (String Split)", "Complex (Regex)"), key="parse_method_radio")
        
        parsed_results = []
        for log_line in raw_logs:
            if parse_type == "Basic (String Split)":
                parsed_results.append(parse_basic_log(log_line))
            else:
                parsed_results.append(parse_complex_log(log_line))
        
        if parsed_results:
            st.subheader("Parsed Log Data (First 10)")
            st.dataframe(pd.DataFrame(parsed_results).head(10)) # Display as DataFrame for better viewing
            st.json(parsed_results[0]) # Show full JSON of first entry
        else:
            st.info("No logs parsed or file was empty.")

# --- Day 7 (Part 2) & Day 8: Generating System Metrics & Storing Locally ---
st.header("3. System Metrics & Local Storage (Day 7.2 & 8)")
st.write("Collect real-time system metrics and save data to CSV or JSON.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Collect Metrics")
    metric_type = st.radio("Select Metric Type:", ("Basic Metrics", "Comprehensive Metrics"), key="metric_type_radio")
    
    if st.button("Collect Metrics Snapshot", key="collect_metrics_button"):
        if metric_type == "Basic Metrics":
            st.session_state.current_metrics = get_system_metrics()
        else:
            st.session_state.current_metrics = get_comprehensive_metrics()
        st.json(st.session_state.current_metrics)
    
    if 'current_metrics' in st.session_state and st.session_state.current_metrics:
        st.subheader("Current Metrics Snapshot")
        st.json(st.session_state.current_metrics)

with col2:
    st.subheader("Save Collected Data")
    save_data_type = st.radio("Data to Save:", ("Current Metrics Snapshot", "Parsed Logs (if available)"), key="save_data_type_radio")
    save_format = st.radio("Save Format:", ("CSV", "JSON"), key="save_format_radio")
    save_filename = st.text_input("Save File Name:", "output.json", key="save_filename_input")

    if st.button("Save Data", key="save_data_button"):
        data_to_save = None
        if save_data_type == "Current Metrics Snapshot" and 'current_metrics' in st.session_state:
            data_to_save = [st.session_state.current_metrics] # Wrap in list for consistency
        elif save_data_type == "Parsed Logs (if available)" and 'parsed_results' in locals() and parsed_results:
            data_to_save = parsed_results
        
        if data_to_save:
            if save_format == "CSV":
                save_metrics_to_csv(data_to_save, save_filename) # This function handles dicts in list
            else:
                save_data_to_json(data_to_save, save_filename)
        else:
            st.warning("No data available to save. Collect metrics or parse logs first.")

# --- Day 10: Visualizing Data ---
st.header("4. Visualizing Data (Day 10)")
st.write("Generate and display plots for CPU usage trends and API latency distributions.")

col3, col4 = st.columns(2)

with col3:
    st.subheader("CPU Usage Trend")
    cpu_num_points = st.number_input("Number of CPU Data Points:", min_value=10, max_value=200, value=60, step=10, key="cpu_num_points_input")
    if st.button("Generate CPU Plot", key="generate_cpu_plot_button"):
        timestamps, cpu_values = generate_dummy_cpu_data(cpu_num_points)
        fig_cpu = plot_cpu_trend(timestamps, cpu_values)
        st.pyplot(fig_cpu) # Display the Matplotlib figure.

with col4:
    st.subheader("API Latency Distribution")
    latency_num_points = st.number_input("Number of Latency Data Points:", min_value=100, max_value=1000, value=500, step=100, key="latency_num_points_input")
    if st.button("Generate Latency Plot", key="generate_latency_plot_button"):
        latency_data = np.random.normal(loc=150, scale=30, size=latency_num_points)
        latency_data = latency_data[latency_data > 0]
        fig_latency = plot_latency_distribution(latency_data)
        st.pyplot(fig_latency) # Display the Matplotlib figure.

st.markdown("---")
st.markdown("### Python Regex Tester (from Day 5)")
st.write("Test your regular expressions against sample log lines. This is a crucial skill for log parsing.")

log_sample_input = st.text_area("Sample Log Line:", 
    "2023-10-26 10:05:30,123 INFO [main] com.example.App - Application started successfully. User: john.doe", 
    height=100, key="regex_log_sample")
regex_pattern_input = st.text_input("Regex Pattern (Python style, use `(?P<name>...)` for groups):", 
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}).*?(?P<level>[A-Z]+).*?(?P<message>Application started successfully).*?User: (?P<user>\w+)", 
    key="regex_pattern_input")

if st.button("Test Regex", key="test_regex_button"):
    try:
        match = re.search(regex_pattern_input, log_sample_input)
        if match:
            st.success("Match Found!")
            st.subheader("Full Match:")
            st.code(match.group(0))
            
            st.subheader("Captured Groups:")
            groups_dict = match.groupdict()
            if groups_dict:
                st.json(groups_dict)
            else:
                st.info("No named capture groups found in the pattern.")
                st.write("Unnamed groups (if any):")
                st.json(match.groups())
        else:
            st.info("No match found.")
    except re.error as e:
        st.error(f"Regex Error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

