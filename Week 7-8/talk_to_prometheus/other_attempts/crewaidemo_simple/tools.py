# Tools: Prometheus Query, File I/O, Docker Runner
import requests, json, os
from crewai.tools import BaseTool
from schemas import Plan, ExecutionResult, Analysis
from config import PROMETHEUS_BASE_URL

class PrometheusQueryTool(BaseTool):
    name: str = "prometheus_query"
    description: str = "Executes a PromQL query against Prometheus. "
    "Arguments: plan of scheam 'Plan' with query (str), parameters (dict) or None, query_type (str, 'query' or 'query_range'), step (str). Returns JSON results."

    # use Plan as an input as it is the output of the planning task
    def _run(self, plan: Plan | dict) -> dict:
        query = plan.get("query",{})
        parameters = plan.get("parameters",{})
        query_type = plan.get("query_type", "query")
        step = plan.get("step", "1m")
        url = f"{PROMETHEUS_BASE_URL}/api/v1/{query_type}"
        params = {"query": query}
        if step:
            params["step"] = step
        if parameters:
            params.update(parameters)
        print(f"Running on Prometheus url: {url} with params: {params}")
        r = requests.get(url, params=params)
        if r.status_code != 200:
            r.raise_for_status()
            return {"error": f"Query failed: {r.text}"}
        return r.json()

class FileStorageTool(BaseTool):
    name: str = "file_store"
    description: str = """Stores/loads JSON results from disk. Actions: 'save' or 'load'. 
    Parameters: action (str), data (dict, for save), filename (str). Returns file path or loaded data."""

    def _run(self, action: str, data: dict | None = None, filename: str = "data.json"):
        if action == "save":
            with open(filename, "w") as f:
                json.dump(data, f)
            return {"saved": filename}
        elif action == "load":
            with open(filename) as f:
                return json.load(f)
        else:
            raise ValueError("Invalid action")