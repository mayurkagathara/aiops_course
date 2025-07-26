#%%
import datetime
import random
import time
import os

module_path = os.path.dirname(os.path.realpath(__file__))

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

#%%
def generate_log_message(level):
    """
    level is from LOG_LEVELS
    this takes level as input and then generate the log meesage
    """
    if level == "INFO":
        user = random.choice(["alice", "bob", "charlie"])
        ip = f"192.168.1.{random.randint(1, 254)}"
        service = random.choice(["auth-service", "data-api"])
        endpoint = random.choice(["/users", "/data", "/status"])
        time_ms = random.randint(50, 500)
        return random.choice(INFO_MESSAGES).\
            format(user=user, ip=ip, service=service, 
                   endpoint=endpoint, time_ms=time_ms)
    elif level in ["ERROR", "WARNING", "DEBUG"]:
        service = random.choice(["auth-service", "data-api", "db-service"])
        error_code = random.choice(["CONN_REFUSED", "TIMEOUT", "AUTH_FAILED"])
        disk_path = random.choice(["/var/log", "/opt/app"])
        reason = random.choice(["Segmentation fault", "NullPointerException"])
        return random.choice(ERROR_MESSAGES).\
            format(service=service, error_code=error_code, 
                   disk_path=disk_path, reason=reason)
    # Add more logic for WARNING, DEBUG etc.
    return "Generic Log message"    

def simulate_log_file(filename="app.log", num_entries=100, interval_seconds=0.1):
    """
    Generates a simulated application log file.
    Args:
        filename (str): The name of the log file to create.
        num_entries (int): The total number of log entries to generate.
        interval_seconds (float): Time delay between generating entries.
    """
    current_time = datetime.datetime.now()
    file_path = os.path.join(module_path, filename)
    with open(file_path, 'w') as logfile:
        for i in range(num_entries):
            level = random.choices(LOG_LEVELS, weights=[0.7, 0.2, 0.08, 0.02], k=1)[0] # Skew towards INFO)
            service = random.choice(["auth-service", "payment-service", "user-api", "inventory-db"])
            message = generate_log_message(level) # Use the function from 6.2

            log_line = f"{current_time.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]} {level} [{service}] {message}\n"
            current_time += datetime.timedelta(seconds=random.uniform(interval_seconds * 0.5, interval_seconds * 1.5))
            # print(log_line)
            logfile.write(log_line)
            # time.sleep(0.01)

if __name__ == "__main__":
    simulate_log_file(num_entries=1000, interval_seconds=0.05)
