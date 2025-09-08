# CrewAI Tasks orchestration
from crewai import Task
from schemas import Plan, ExecutionResult, Analysis
from agents import PlanningAgent, ExecutorAgent, AnalyzerAgent

PlanTask = Task(
    description ="""
    Plan PromQL query based on user's natural language input {input}. 
    This task involves interpreting the user's intent,
    identifying the appropriate PromQL constructs, and generating a detailed query plan. 
    """,
    agent=PlanningAgent,
    output_json=Plan,
    expected_output="The output should be a JSON object containing "
    "the PromQL query string with parameters, the query type (e.g., 'query', 'query_range'), " 
    "parameters are optional and different per query_type like 'start', 'end', 'step', 'time', etc "
    "and an optional step size if applicable."
)

ExecuteTask = Task(
    description=f"""
    Get the output from the PlanTask and use it as is.
    Execute the planned PromQL query against Prometheus only using tool.
    RULES: 
    - Use PrometheusQueryTool to run the query.
    - Do not answer with dummy data if no data is returned from Prometheus.
    """,
    agent=ExecutorAgent,
    # context=[PlanTask],
    output_json=ExecutionResult,
    expected_output="The output should be a JSON object containing the query results, a boolean indicating if the results were stored in a file, and the file path if applicable."
)

AnalyzeTask = Task(
    description="""
    Analyze the results of the PromQL query. This task processes the raw data, identifies key insights, and
    generates a summary that includes statistical analysis and actionable recommendations. The goal is to
    provide users with a clear understanding of the data and its implications.
    """,
    agent=AnalyzerAgent,
    # context=[ExecuteTask],
    output_json=Analysis,
    expected_output="The output should be a JSON object containing a summary of the analysis, " 
    "statistical data as a dictionary, "
    "and a list of actionable recommendations."
)