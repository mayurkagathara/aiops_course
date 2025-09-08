import requests
from datetime import datetime, timedelta
from typing import Dict
from config_schema import *
from config import (
    PROMETHEUS_BASE_URL,
)

def PrometheusQueryTool(plan: Dict) -> Dict:
    try:
        # Use Pydantic model for robust parsing and validation of the plan
        query_plan = PromQLPlan(**plan)
        print(
            f"--- TOOL: Executing PromQL plan: {query_plan.model_dump_json()} ---"
        )

        url = f"{PROMETHEUS_BASE_URL}/api/v1/{query_plan.query_type}"

        # Build params, including dynamic start/end for range queries
        params = {"query": query_plan.query}
        if query_plan.query_type == "query_range":
            if query_plan.parameters:
                # A real implementation would parse timeframes like "15m"
                # For simplicity, we'll assume they are pre-calculated.
                params.update(query_plan.parameters)
            else:  # Default to last 15 minutes if not specified
                end_time = datetime.now(datetime.timezone.utc)
                start_time = end_time - timedelta(minutes=15)
                params["start"] = start_time.isoformat() + "Z"
                params["end"] = end_time.isoformat() + "Z"
                params["step"] = "1m"
        
        print(f"--- TOOL: Querying Prometheus at {url} with params {params} ---")

        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        import traceback
        return {"success": False, "message": f"failed: {e} {traceback.format_exc()}"}
