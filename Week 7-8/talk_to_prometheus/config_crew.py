from crewai import Agent, Task, LLM
from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    AGENT_VERBOSE,
    MAX_AGENT_ITERATIONS,
    USE_LOCAL_LLM
)
from langchain_openai import ChatOpenAI
from config_schema import *

# --- 1. Configuration ---
# PROMETHEUS_BASE_URL = os.environ.get("PROMETHEUS_URL", "http://localhost:9090")

USE_LOCAL_LLM = False

if USE_LOCAL_LLM:
    llm = LLM(
        model="ollama/qwen2.5:1.5b",
        base_url="http://localhost:11434"
    )
else:
    llm = ChatOpenAI(
        model=OPENROUTER_MODEL,
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1"
    )

# --- 4. Agent Definitions ---
# (Agent definitions are solid, no changes needed)
PlanningAgent = Agent(
    verbose = AGENT_VERBOSE,
    role="planner",
    goal="Convert natural language query from user into detailed PromQL",
    llm=llm,
    backstory="The PlanningAgent is designed to bridge the gap "
    "between human intent and machine execution. "
    "It interprets user queries, identifies the underlying requirements, "
    "and formulates a precise PromQL query. ",
    max_iter= MAX_AGENT_ITERATIONS
)

AnalyzerAgent = Agent(
    verbose = AGENT_VERBOSE,
    role="analyzer",
    goal="Analyze Prometheus query results, extract meaningful insights, "
    "and provide actionable recommendations based on the data.",
    llm=llm,
    # tools=[FileStorageTool()],
    backstory="The AnalyzerAgent is the system's intelligence layer. "
    "It processes the raw results from Prometheus, identifies patterns, "
    "and generates insights that are both actionable and easy to understand. "
    "This agent ensures that users can make informed decisions based on the data.",
    max_iter= MAX_AGENT_ITERATIONS
)
# --- 6. Task and Flow Definition ---
# Define tasks with unique names
PlanTask = Task(
    description ="""
    Plan PromQL query based on user's natural language input {original_query}. 
    This task involves interpreting the user's intent,
    identifying the appropriate PromQL constructs.
    STRICTLY use the unix timestamp for any time parameters. 
    In the output json, if the query_type is "query_range",
    include "start", "end" (both as unix timestamps) and "step" in parameters.
    """,
    agent=PlanningAgent,
    output_json=PromQLPlan,
    expected_output="The output should be a JSON object containing "
    "the PromQL query string with parameters, the query type (e.g., 'query', 'query_range'), " 
    "parameters are optional and different per query_type like 'start', 'end', 'step', 'time', etc "
    "and an optional step size if applicable."
)

AnalyzeTask = Task(
    description=""" For given user's query: {original_query}, 
    Analyze the results of the PromQL query. 
    ```json
    {prometheus_results}
    ```
    This task processes the raw data, identifies key insights, and
    generates a summary that includes statistical analysis and actionable recommendations. The goal is to
    provide users with a clear understanding of the data and its implications.
    """,
    agent=AnalyzerAgent,
    expected_output="The output should be in easy to understand language " 
    "Provide some statistics bullet points, "
    "and a list of actionable recommendations. "
    "Do not give too long answers, keep it concise and to the point."
)
