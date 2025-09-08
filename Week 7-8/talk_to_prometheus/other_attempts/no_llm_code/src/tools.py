# Tools: Prometheus HTTP access, simple file store, runner for heavy analysis
import os, json, subprocess
from typing import Dict, Any
import requests
import config
from utils import estimate_size_bytes

class PrometheusTool:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or config.PROMETHEUS_BASE_URL

    def query(self, promql: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/v1/query"
        r = requests.get(url, params={"query": promql}, timeout=15)
        r.raise_for_status()
        return r.json()

    def query_range(self, promql: str, start: int, end: int, step: int) -> Dict[str, Any]:
        url = f"{self.base_url}/api/v1/query_range"
        r = requests.get(url, params={"query": promql, "start": start, "end": end, "step": step}, timeout=30)
        r.raise_for_status()
        return r.json()

class FileStoreTool:
    def __init__(self, path: str = None):
        self.path = path or config.DATA_FILE_PATH
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                json.dump({"__comments": "auto-created", "data": {}}, f, indent=2)

    def write(self, key: str, payload: Dict[str, Any], comment: str = None) -> Dict[str, Any]:
        with open(self.path, 'r', encoding='utf-8') as f:
            doc = json.load(f)
        if "data" not in doc:
            doc["data"] = {}
        doc["data"][key] = payload
        if comment:
            doc["__comments"] = comment
        tmp = self.path + ".tmp"
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(doc, f, indent=2)
        os.replace(tmp, self.path)
        approx = estimate_size_bytes(payload)
        return {"storage": "file", "key": key, "approx_bytes": approx}

    def read(self, key: str):
        with open(self.path, 'r', encoding='utf-8') as f:
            doc = json.load(f)
        return doc.get("data", {}).get(key)

class PythonRunnerTool:
    def __init__(self, prefer_docker: bool = None):
        self.prefer_docker = config.DOCKER_PREFER if prefer_docker is None else prefer_docker

    def run_job(self, data_ref: Dict[str, Any], analysis_args: Dict[str, Any] = None) -> Dict[str, Any]:
        analysis_args = analysis_args or {}
        file_path = config.DATA_FILE_PATH
        key = data_ref.get('key')
        if self.prefer_docker:
            img = "talk-prom-analysis"
            cmd = [
                "docker", "run", "--rm",
                "-v", f"{os.path.abspath(os.path.dirname(file_path))}:/data",
                img,
                "python", "/runner/job.py",
                "--file", f"/data/{os.path.basename(file_path)}",
                "--key", key
            ]
        else:
            cmd = ["python", "analysis-runner/job.py", "--file", file_path, "--key", key]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
            out = proc.stdout.strip()
            if not out:
                return { "error": "no output from runner", "stdout": proc.stdout, "stderr": proc.stderr }
            return json.loads(out)
        except subprocess.CalledProcessError as e:
            return { "error": "runner-failed", "stdout": e.stdout, "stderr": e.stderr }
