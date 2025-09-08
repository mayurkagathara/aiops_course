# Utilities
import re, json, time
from datetime import datetime

def parse_duration_to_seconds(text: str) -> int:
    if not text:
        return 0
    m = re.match(r'^(\d+)([smhd])$', text.strip())
    if not m:
        return 0
    val = int(m.group(1))
    unit = m.group(2)
    if unit == 's': return val
    if unit == 'm': return val * 60
    if unit == 'h': return val * 3600
    if unit == 'd': return val * 86400
    return 0

def now_seconds() -> int:
    return int(time.time())

def estimate_size_bytes(obj) -> int:
    try:
        s = json.dumps(obj)
        return len(s.encode('utf-8'))
    except Exception:
        return 0

def simple_promql_sanitize(promql: str) -> str:
    if not promql:
        return promql
    promql = promql.strip().rstrip(';')
    return promql
