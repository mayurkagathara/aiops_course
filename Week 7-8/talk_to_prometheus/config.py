# Centralized configuration for Talk to Prometheus
import os
from dotenv import load_dotenv
load_dotenv('.env.example')

PROMETHEUS_BASE_URL = os.getenv("PROMETHEUS_BASE_URL", "http://localhost:9090")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "qwen/qwen3-235b-a22b:free")
MAX_TOOL_CALLS_PER_TASK = int(os.getenv("MAX_TOOL_CALLS_PER_TASK", 2))
MAX_AGENT_ITERATIONS = int(os.getenv("MAX_AGENT_ITERATIONS", 2))
AGENT_VERBOSE = True
USE_LOCAL_LLM = False