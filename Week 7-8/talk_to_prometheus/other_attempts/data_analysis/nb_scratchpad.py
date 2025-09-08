import requests

def run(query: str, start: int, end: int, step: int) -> str:
        """Use the tool."""
        VM_URL = "http://localhost:9090/api/v1"
        url = f"{VM_URL}/query_range"
        params = {"query": query, "start": start, "end": end, "step": step, "limit": 100} 

        print(f"{'='*20}\nURL: {url}\nParams: {params}\n{'='*20}")

        resp = requests.get(url, params=params, timeout=60, verify=False)
        if resp.status_code != 200:
            return {"error": f"Query failed: {resp.text}"}

        data = resp.json().get("data", {}).get("result", [])
        if not data:
            return {"error": "No data found for given host/time range"}

        return data

from datetime import datetime
now = int(datetime.now().timestamp())
five_min_ago = now - 5*60
print(run(query= "node_memory_MemAvailable_bytes", start= five_min_ago, end= now , step= "15s"))

PROMETHEUS_BASE_URL="http://localhost:9090"
def run_2(query: str, query_type: str = "query", step: str | None = None) -> dict:
        url = f"{PROMETHEUS_BASE_URL}/api/v1/{query_type}"
        params = {"query": query}
        if step:
            params["step"] = step
        print(url, params)
        print(f"{'='*20}\nURL: {url}\nParams: {params}\n{'='*20}")
        r = requests.get(url, params=params, verify=False)
        r.raise_for_status()
        return r.json()
print(run_2(query= "((node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes) * 100", 
            query_type="query_range",
            step="15s"
            ))
# {"query": "((node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes) * 100", "query_type": "query_range", "step": "15s"}