from langchain.schema import Tool
from langchain.chat_models import ChatOpenAI
from tools import PrometheusQueryTool, FileStorageTool
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL

# Initialize the LLM
llm = ChatOpenAI(
    model=OPENROUTER_MODEL,
    openai_api_key=OPENROUTER_API_KEY,
    temperature=0.7
)

# Define tools
prometheus_tool = PrometheusQueryTool()
file_storage_tool = FileStorageTool()

# Define the Planning Tool
planning_tool = Tool(
    name="PlanningTool",
    description="Converts natural language queries into PromQL plans.",
    func=lambda input: llm.predict(f"Plan a PromQL query for: {input}")
)

# Define the Execution Tool
execution_tool = Tool(
    name="ExecutionTool",
    description="Executes PromQL queries and stores results.",
    func=prometheus_tool._run
)

# Define the Analysis Tool
analysis_tool = Tool(
    name="AnalysisTool",
    description="Analyzes PromQL query results and provides insights.",
    func=file_storage_tool._run
)
