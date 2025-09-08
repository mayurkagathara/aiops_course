from langchain.tools import BaseTool
import requests
import json
from config import PROMETHEUS_BASE_URL

class PrometheusQueryTool(BaseTool):
    name = "prometheus_query"
    description = "Executes a PromQL query against Prometheus."

    def _run(self, query: str) -> dict:
        """
        Executes a PromQL query.
        Args:
            query (str): The PromQL query to execute.
        Returns:
            dict: The query results.
        """
        url = f"{PROMETHEUS_BASE_URL}/api/v1/query"
        params = {"query": query}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"Prometheus query failed: {response.text}")
        return response.json()

class FileStorageTool(BaseTool):
    name = "file_storage"
    description = "Saves or loads JSON data to/from a file."

    def _run(self, action: str, data: dict = None, filename: str = "results.json") -> dict:
        """
        Saves or loads JSON data.
        Args:
            action (str): "save" or "load".
            data (dict): Data to save (if action is "save").
            filename (str): File name.
        Returns:
            dict: File path or loaded data.
        """
        if action == "save":
            with open(filename, "w") as f:
                json.dump(data, f)
            return {"file_saved": filename}
        elif action == "load":
            with open(filename, "r") as f:
                return json.load(f)
        else:
            raise ValueError("Invalid action. Use 'save' or 'load'.")
