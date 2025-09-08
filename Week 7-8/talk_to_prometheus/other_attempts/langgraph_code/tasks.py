# LangGraph Tasks orchestration
from langgraph import Task
from agents import planning_node, execution_node, analysis_node

# Define the Planning Task
PlanTask = Task(
    name="PlanTask",
    description="Generates a PromQL query plan from natural language input.",
    node=planning_node
)

# Define the Execution Task
ExecuteTask = Task(
    name="ExecuteTask",
    description="Executes the PromQL query and stores the results.",
    node=execution_node
)

# Define the Analysis Task
AnalyzeTask = Task(
    name="AnalyzeTask",
    description="Analyzes the query results and provides insights.",
    node=analysis_node
)
