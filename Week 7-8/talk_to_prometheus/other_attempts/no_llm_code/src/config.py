# Simple settings
import os
from dotenv import load_dotenv
load_dotenv('.env.example')

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "qwen-7b-instruct")
PROMETHEUS_BASE_URL = os.getenv("PROMETHEUS_BASE_URL", "http://localhost:9090")
INMEMORY_MAX_BYTES = int(os.getenv("INMEMORY_MAX_BYTES", "2097152"))
DATA_FILE_PATH = os.getenv("DATA_FILE_PATH", "./data/run.json")
DOCKER_PREFER = os.getenv("DOCKER_PREFER", "false").lower() in ("1","true","yes")
