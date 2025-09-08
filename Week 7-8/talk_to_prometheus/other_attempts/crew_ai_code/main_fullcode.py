"""
Production-Grade PromQL Generation Application using Native crewAI Flow.

This script implements a multi-agent crew to convert natural language queries
into valid and executable PromQL queries. It uses the native `crewai.flow`
module with a router to handle syntax validation and a controlled retry loop.

Corrections from previous version:
1.  Replaced the incorrect `crewai_flow` library with the official `crewai.flow` module.
2.  Implemented a `router` function to manage the conditional Code -> Validate loop.
3.  Fixed the `PrometheusQueryTool` to correctly handle parameters for range queries.
4.  Ensured all agents and tasks correctly interact with a shared context dictionary.
"""

import os
import requests
import json
import uuid
from datetime import datetime, timedelta, timezone
from crewai import Agent, Task, Crew, Process
from crewai.flow import Flow, start, listen, router
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Optional, Any, Tuple, Type
from dataclasses import dataclass
from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    AGENT_VERBOSE,
    MAX_AGENT_ITERATIONS,
)
from langchain_openai import ChatOpenAI

# --- 1. Configuration ---
MAX_RETRIES = MAX_AGENT_ITERATIONS  # Max retries for validation failures
PROMETHEUS_BASE_URL = os.environ.get("PROMETHEUS_URL", "http://localhost:9090")

llm = ChatOpenAI(
    model=OPENROUTER_MODEL,
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
)

# --- 2. State Management & Pydantic Schemas ---

class PromParams(BaseModel):
    start: Optional[int] = None  # Unix timestamp
    end: Optional[int] = None    # Unix timestamp
    step: Optional[str] = "1m"  # Step duration like '1m', '5m'

class PromQLPlan(BaseModel):
    query: str
    query_type: str = "query_range"
    parameters: PromParams = None

class PromQLWorkflowState(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    original_query: str = ""
    promql_plan: PromQLPlan = None
    validation_result: bool = None
    validation_feedback: Optional[str] = None
    final_prometheus_result: Optional[Dict] = None
    final_answer: Optional[str] = None
    retry_count: int = 0
    next_task: Optional[str] = None

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

# Define the flow using decorators
class PromQLFlow(Flow[PromQLWorkflowState]):
    """A flow class for converting natural language to PromQL queries."""
    
    def __init__(self, original_query: str = "", retry_count: int = 1):
        """Initialize flow with required tasks and agents."""
        super().__init__()
        # Store task-agent pairs
        self.task_agents = {
            "code": (PlanTask, PlanningAgent),
            "analyze": (AnalyzeTask, AnalyzerAgent)
        }
        self.state.original_query = original_query
        self.state.retry_count = retry_count
        
    @start()
    def initial_step(self):
        return "Starting process"

    @listen(initial_step)
    def generate_query(self) -> Dict:
        """Start by analyzing the user query."""
        coding_task, coding_agent = self.task_agents["code"]
        print(f"{'='*20}",coding_task, coding_agent, f"{'='*20}")
        print(f"--- FLOW: Starting analysis for query: {self.state.original_query} ---")
        
        # Create crew for this task
        generate_query_crew = Crew(
            agents=[coding_agent],
            tasks=[coding_task],
            process=Process.sequential,
            verbose=True,
        )
        result = generate_query_crew.kickoff(inputs={"original_query": self.state.original_query})
        print(result)
        # ####
        # import json
        # raw_result = """{"query": "(node_memory_MemTotal_bytes - node_memory_MemFree_bytes - node_memory_Buffers_bytes - node_memory_Cached_bytes) / node_memory_MemTotal_bytes * 100", "query_type": "query_range", "parameters": {"start": 1718698500, "end": 1718700000, "step": "1m"}}"""
        # self.state.promql_plan = PromQLPlan(**json.loads(raw_result))
        # ####
        self.state.promql_plan = PromQLPlan(**json.loads(result.raw))
        
        print("\n\ngenerated query ", result.raw)
        return self.state
    
    @router(generate_query)
    def validation_router(self, state) -> str:
        """try to run the query and take routing decision based on that."""
        try:
            print("plan to validate ", self.state.promql_plan)
            plan = self.state.promql_plan.model_dump_json()
            
            result = PrometheusQueryTool(json.loads(plan))
            if result.get("success", True):
                self.state.validation_result = True
                self.state.validation_feedback = "Query executed successfully."
                self.state.final_prometheus_result = result
                return "analyze_results"
            else:
                self.state.validation_result = False
                self.state.validation_feedback = result.get("message", "Unknown error")
                self.state.retry_count += 1

                if self.state.retry_count <= 2:
                    return "retry_generate_query"
                else:
                    return "handle_failure"
                
        except Exception as e:
            self.state.validation_result = False
            self.state.validation_feedback = str(e)
            return "handle_failure"
    
    @listen("retry_generate_query")
    def retry_query_generation(self):
        return self.generate_query()
        

    @listen("analyze_results")
    def analyze_prom_results(self) -> Dict:
        """Analyze the prometheus results."""
        analysis_task, analysis_agent = self.task_agents["analyze"]
        prometheus_results = self.state.final_prometheus_result
        print(f"--- FLOW: Starting analysis for reults: {prometheus_results} ---")
        
        # Create crew for this task
        analysis_crew = Crew(
            agents=[analysis_agent],
            tasks=[analysis_task],
            process=Process.sequential,
            verbose=True,
        )
        result = analysis_crew.kickoff(
            inputs={
                "prometheus_results": prometheus_results, 
                "original_query": self.state.original_query,
                }
        )
        self.state.final_answer = result.raw
        print("generated answer ", result.raw)
        return self.state

    
    @listen("handle_failure")
    def handle_failure_message(self) -> Dict:
        """Handle validation failure after max retries."""
        self.state.final_answer = (
            "❌ Failed to generate a valid query after several attempts. "
            f"Last validation feedback: {self.state.validation_feedback}"
        )
        return self.state
        

# # Create flow instance
# flow = PromQLFlow()

# --- 7. Main Orchestrator ---
if __name__ == "__main__":
    print("🚀 Starting the Prometheus PromQL Generation Flow...")
    
    try:
        # Create and run flow directly
        user_query = f"Analyze the Memory usage for the last 15 minutes. current epoch is {int(datetime.now().timestamp())}"
        flow = PromQLFlow(original_query=user_query, retry_count=1)
        flow.plot()

        user_input = input(r"continue? (y\n): ")

        if user_input == "y":
            final_state = flow.kickoff()

        print("\n\n########################")
        print("## ✅ Flow Run Completed!")
        print("########################\n")

        # # Print the final answer or error message
        # if final_state.get("final_answer"):
        #     print("Final Answer:")
        #     print(final_state["final_answer"])
        # elif final_state.get("validation_result", {}).get("is_valid") is False:
        #     print("❌ Failed to generate a valid query after several attempts.")
        #     print(f"Last validation feedback: {final_state['validation_result']['feedback']}")
        # else:
        #     print("❌ Unexpected error occurred")

        try:
            print("\n--- Final Workflow State ---\n", final_state)
            print(json.dumps(final_state.model_dump_json(), indent=2))
        except Exception as e:
            print(str(e))
        
        try:
            import pickle
            with open("final_state.pkl", "wb") as f:
                pickle.dump(final_state, f)
        except Exception as e:
            print(f"problem in pickle", str(e))

    except Exception as e:
        import traceback
        print(f"\n❌ Error during workflow execution: {str(e)} \n {traceback.format_exc()}")
