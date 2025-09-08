#!/usr/bin/env python3
"""
Python log generator that writes realistic app logs (NOT JSON) embedding key fields.
Output format:
YYYY-MM-DD HH:MM:SS,mmm LEVEL [application_name] (customer=<id>, customer_name=<name>, environment=<env>, log_type=<type>) <message>
"""
import os
import random
from datetime import datetime, timedelta
import time

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
LOG_FILE_PATH = os.path.join(FILE_PATH, "logs/app.log")

CUSTOMERS = [
    ("cust001", "Acme Corp"),
    ("cust002", "Beta Industries"),
    ("cust003", "Gamma Labs"),
    ("cust004", "Delta Systems"),
    ("cust005", "Omega Retail")
]

ENVIRONMENTS = ["dev", "test", "stage", "prod"]
APPLICATIONS = ["auth-service", "payment-service", "inventory-service", "user-service", "reporting-service"]
LOG_TYPES = ["app", "lb", "tomcat"]
LEVELS = ["INFO", "WARN", "ERROR"]
NUM_LOG_MESSAGES = 100

API_PATHS = [
    "/auth/login", "/auth/logout", "/payments/charge", "/payments/refund",
    "/inventory/items", "/inventory/update", "/users/profile", "/reports/daily"
]

ERROR_MESSAGES = [
    "DB connection timeout",
    "NullPointerException at ServiceLayer",
    "Invalid token provided",
    "Upstream service unavailable",
    "Cache miss; fallback to DB",
    "Circuit breaker open; request denied",
    "Failed to parse JSON payload",
    "Permission denied for user role",
    "Could not establish a connection to the primary database. Connection refused by host.",
    "SQL transaction rollback due to a deadlock detected on table 'user_profiles'.",
    "Query execution failed: Unique key constraint 'UQ_order_id' violated.",
    "Failed to initialize database connection pool; max pool size exceeded.",
    "A race condition was detected while updating the inventory count for product_id 7891.",
    "Request to payment gateway API failed with status 503 Service Unavailable.",
    "Request to downstream service 'analytics-engine' exceeded the configured timeout of 5000ms.",
    "SSL handshake failed when connecting to external service 'inventory-api'.",
    "Upstream service 'user-auth-service' returned a non-2xx status code: 404 Not Found for user_id 123.",
    "DNS lookup for service 'notification-service.internal' failed. Host not found.",
    "Authentication failed for user 'support@example.com': Invalid password provided.",
    "JWT validation failed: Token signature is invalid. The token may have been tampered with.",
    "User 'guest_user' attempted to access a restricted resource '/api/v1/admin/dashboard' without sufficient privileges.",
    "OAuth2 token refresh failed for client ID 'webapp-client'. The refresh token is expired or has been revoked.",
    "Caught an unhandled java.lang.IllegalArgumentException: The 'limit' parameter cannot be less than zero.",
    "java.lang.OutOfMemoryError: Java heap space. The application will be restarted.",
    "python.KeyError: 'user_email' not found in incoming JSON request payload.",
    "python.TypeError: unsupported operand type(s) for +: 'int' and 'NoneType' in function calculate_total.",
    "java.lang.IllegalStateException: Cannot transition order status from 'SHIPPED' to 'CANCELLED'.",
    "Uncaught exception in thread 'main-event-loop': java.lang.StackOverflowError.",
    "Failed to write to log file '/var/log/app/application.log'. Permission denied.",
    "python.FileNotFoundError: [Errno 2] No such file or directory: '/tmp/uploads/invoice-2025-09-04.pdf'.",
    r"Disk space is critically low on volume '/data'. Less than 1% free space remaining.",
    "java.io.IOException: Error processing uploaded file. The file appears to be corrupted or is not a valid CSV.",
    "Required environment variable 'API_SECRET_KEY' is not set. Application cannot start.",
    "Configuration file 'settings.prod.json' not found. Falling back to default application settings.",
    "Could not decrypt secret 'DB_PASSWORD' from the secrets manager. Check IAM role and permissions.",
    "Message queue 'email-notifications' is backed up with over 10,000 pending messages.",
    r"High CPU utilization detected, currently at 98% for over 5 minutes.",
    "Thread pool 'http-nio-8080-exec' is exhausted. Cannot accept new incoming connections."
]

def random_message(level: str) -> str:
    if level == "INFO":
        path = random.choice(API_PATHS)
        ms = random.randint(20, 1000)
        return f"Request to {path} completed in {ms}ms"
    elif level == "WARN":
        path = random.choice(API_PATHS)
        ms = random.randint(800, 3000)
        return f"Slow response on {path}; took {ms}ms"
    else:  # ERROR
        return random.choice(ERROR_MESSAGES)

def main(out_path: str = LOG_FILE_PATH, n_lines: int = NUM_LOG_MESSAGES):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # generate timestamps over the last 7 days
    now = datetime.now()
    start = now - timedelta(days=7)

    with open(out_path, "a", encoding="utf-8", newline="\n") as f:
        for _ in range(n_lines):
            cust_id, cust_name = random.choice(CUSTOMERS)
            env = random.choice(ENVIRONMENTS)
            app = random.choice(APPLICATIONS)
            ltype = random.choice(LOG_TYPES)
            level = random.choices(LEVELS, weights=[0.7, 0.2, 0.1])[0]

            # random timestamp
            delta = random.random() * (now - start).total_seconds()
            ts = start + timedelta(seconds=delta)
            ts_str = ts.strftime("%Y-%m-%d %H:%M:%S") + f",{random.randint(0,999):03d}"

            msg = random_message(level)

            line = (f"{ts_str} {level} [{app}] "
                    f"(customer={cust_id}, customer_name={cust_name}, environment={env}, log_type={ltype}) "
                    f"{msg}")
            f.write(line + "\n")

if __name__ == "__main__":
    main()
