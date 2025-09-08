from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import JSONResponse
from typing import Dict, Any
from datetime import datetime, timedelta
import json
import os
from threading import Lock

# ----------------------
# CONFIGURATION
# ----------------------
API_KEY = "MY_SECURE_API_KEY"
API_KEY_NAME = "X-API-Key"
ALERTS_FILE = "alerts.json"
ALERT_STORM_FILE = "alert_storm.json"
SUPPRESSED_FILE = "suppressed.json"

RATE_LIMIT_COUNT = 5         # Alerts per minute
SUPPRESSION_THRESHOLD = 3    # Alerts per host per minute
SUPPRESSION_TIME = 60        # Seconds

# ----------------------
# GLOBALS
# ----------------------
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
lock = Lock()

# Store recent alert timestamps for rate limiting
recent_alerts_times = []

# Track host alert times for suppression
host_alerts_times = {}

# ----------------------
# UTILITY FUNCTIONS
# ----------------------
def load_json(filename: str) -> list:
    """Load JSON data from file, return empty list if not exists."""
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_json(filename: str, data: list):
    """Save JSON data to file."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def authenticate(api_key: str = Depends(api_key_header)):
    """API Key authentication dependency."""
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key

def is_rate_limited() -> bool:
    """Check if we have exceeded the rate limit for all alerts."""
    now = datetime.utcnow()
    # Remove entries older than 1 min
    global recent_alerts_times
    recent_alerts_times[:] = [t for t in recent_alerts_times if (now - t).seconds < 60]

    if len(recent_alerts_times) >= RATE_LIMIT_COUNT:
        return True
    return False

def add_rate_limit_entry():
    """Record a new alert timestamp for rate limiting."""
    recent_alerts_times.append(datetime.utcnow())

def is_host_suppressed(host: str) -> bool:
    """Check if host is currently suppressed."""
    now = datetime.utcnow()
    # Clean up expired suppression
    expired_hosts = [h for h, t in host_alerts_times.items() if (now - t).seconds > SUPPRESSION_TIME]
    for h in expired_hosts:
        del host_alerts_times[h]

    return host in host_alerts_times

def record_host_alert(host: str) -> bool:
    """
    Record alert for host. 
    If host crosses threshold, suppress it and return True for suppression.
    """
    if not hasattr(record_host_alert, "history"):
        record_host_alert.history = {}  # {host: [timestamps]}

    now = datetime.utcnow()
    record_host_alert.history.setdefault(host, [])
    record_host_alert.history[host] = [t for t in record_host_alert.history[host] if (now - t).seconds < 60]
    record_host_alert.history[host].append(now)

    if len(record_host_alert.history[host]) > SUPPRESSION_THRESHOLD:
        host_alerts_times[host] = now  # Suppress for next 60s
        return True
    return False

def update_or_add_alert(alert: Dict[str, Any], filename: str):
    """Deduplicate by 'identifier' and update if exists, else add."""
    alerts = load_json(filename)
    for idx, existing in enumerate(alerts):
        if existing["identifier"] == alert["identifier"]:
            alerts[idx] = alert  # Update existing alert
            save_json(filename, alerts)
            return
    alerts.append(alert)
    save_json(filename, alerts)

# ----------------------
# FASTAPI APP
# ----------------------
app = FastAPI(title="AIOps Alerts API", version="1.0")

@app.post("/alerts")
async def receive_alert(request: Request, api_key: str = Depends(authenticate)):
    """
    Receive alerts with JSON payload.
    Apply rate limit, deduplication, and host suppression.
    """
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    # 1️⃣ Validate mandatory 'identifier' field
    if "identifier" not in payload:
        raise HTTPException(status_code=400, detail="'identifier' field is required")

    # 2️⃣ Validate 'host' field existence for suppression logic
    if "host" not in payload:
        raise HTTPException(status_code=400, detail="'host' field is required")

    now = datetime.utcnow()
    payload["_metadata"] = {
        "received_at": now.isoformat(),
        "source_ip": request.client.host
    }

    with lock:
        # 3️⃣ Host suppression check
        if is_host_suppressed(payload["host"]):
            suppressed_alerts = load_json(SUPPRESSED_FILE)
            suppressed_alerts.append(payload)
            save_json(SUPPRESSED_FILE, suppressed_alerts)
            return JSONResponse(status_code=200, content={"status": "suppressed", "reason": "Host suppressed"})

        # 4️⃣ Record host alert and see if suppression should be applied
        if record_host_alert(payload["host"]):
            suppressed_alerts = load_json(SUPPRESSED_FILE)
            suppressed_alerts.append(payload)
            save_json(SUPPRESSED_FILE, suppressed_alerts)
            return JSONResponse(status_code=200, content={"status": "suppressed", "reason": "Suppression threshold reached"})

        # 5️⃣ Rate limiting check
        if is_rate_limited():
            storm_alerts = load_json(ALERT_STORM_FILE)
            storm_alerts.append(payload)
            save_json(ALERT_STORM_FILE, storm_alerts)
            return JSONResponse(status_code=429, content={"status": "storm", "reason": "Rate limit exceeded"})

        # 6️⃣ Add to alerts.json with deduplication
        add_rate_limit_entry()
        update_or_add_alert(payload, ALERTS_FILE)

    return {"status": "stored", "identifier": payload["identifier"]}

