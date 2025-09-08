import json
from crewai import Crew, Process
from crewai.flow import Flow, start, listen, router
from typing import Dict
from config import (
    MAX_AGENT_ITERATIONS,
)
from config_schema import *
from config_crew import *
from tools import *

MAX_RETRIES = MAX_AGENT_ITERATIONS  # Max retries for validation failures

# Define the flow using decorators
class PromQLFlow(Flow[PromQLWorkflowState]):
    """A flow class for converting natural language to PromQL queries."""
    
    def __init__(self, original_query: str = "", retry_count: int = MAX_RETRIES):
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