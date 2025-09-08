import os
import pandas as pd
from typing import Optional
from pydantic import BaseModel
import requests
# LangChain and CrewAI imports
# from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, LLM
from crewai.tools import BaseTool
from dotenv import load_dotenv
load_dotenv()

# --- 1. LLM and Tool Definitions ---

llm = LLM(
    model="openrouter/qwen/qwen3-235b-a22b:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

# Initialize the Ollama language model
# llm = LLM(
#     model="ollama/qwen2.5:1.5b",
#     base_url="http://localhost:11434"
# )
# llm = Ollama(model="qwen2.5:1.5b")

class QueryRangeExecutor(BaseTool):
    name: str = "QueryExecutor"
    description: str = "Use this to run the query_range for given prometheus metric."
    
    def _run(self, query: str, start: int, end: int, step: int) -> str:
        """Use the tool."""
        VM_URL = "http://localhost:9090/api/v1"
        url = f"{VM_URL}/query_range"
        params = {"query": query, "start": start, "end": end, "step": step, "limit": 100} 

        resp = requests.get(url, params=params, timeout=60)
        if resp.status_code != 200:
            return {"error": f"Query failed: {resp.text}"}

        data = resp.json().get("data", {}).get("result", [])
        if not data:
            return {"error": "No data found for given host/time range"}

        return data

# A list of the tools available to our agent.
# tools = [incident_rag_tool, AutomationRunookSearchTool()]

# --- 2. CrewAI Agent and Task Definitions ---

# Define the Agent
# This agent's backstory is updated to reflect its new ability to read files.
query_executor_agent = Agent(
    role = "Prometheus Query Executor",
    goal = "To run the prometheus query and return the results",
    backstory= "You are expert in using prometheus query. "
        "your role is to understand the user's {query} in Natural language. "
        "And convert them to prometheus query and run the query." 
        "you provide the results in detailed manner. ",
    llm = llm,
    allow_delegation= False,
    verbose = True,
    tools=[QueryRangeExecutor()],
)

query_execution_task = Task(
    agent = query_executor_agent,
    description = """
        1. understand the user's {query}.
        2. convert it to prometheus query_range.
        3. Prepare the arguments for the tool in below format,
        {
            "query": "prometheus query_range",
            "start": start_time_in_epoch,
            "end": end_time_in_epoch,
            "step": step_in_seconds
        }
        4. Execute the tool and parse, understand the output. 
        5. STRICTLY do not ask the followup questions or do not ask more information from user. 
    """,
    expected_output = "clear and concise answer to the user's {query}",
)
# --- 3. Crew Setup and Execution ---
query = input("User: ")
support_crew = Crew(
    agents=[query_executor_agent],
    tasks=[query_execution_task],
    planning=False,
    # planning_llm=llm,
    verbose=True
)
print("--- Starting CrewAI Application ---")
result = support_crew.kickoff(
    inputs={"query": query}
)
print("\n--- Final Output ---")
print(result)
