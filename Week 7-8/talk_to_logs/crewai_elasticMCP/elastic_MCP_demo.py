from crewai import Agent, LLM, Task, Crew, Process
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters  # For Stdio Server
from langchain_openai import ChatOpenAI
from config import OPENROUTER_MODEL, OPENROUTER_API_KEY, USE_LOCAL_LLM

USE_LOCAL_LLM = False

if USE_LOCAL_LLM:
    llm = LLM(model="ollama/qwen2.5:1.5b", base_url="http://localhost:11434")
else:
    llm = ChatOpenAI(
        model=OPENROUTER_MODEL,
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1",
    )

# Example server_params (choose one based on your server type):
# 1. Stdio Server:
server_params = StdioServerParameters(
    command="docker",
    # run -i --rm -e ES_URL docker.elastic.co/mcp/elasticsearch stdio
    args=[
        "run",
        "-i",
        "--rm",
        "-e",
        "ES_URL",
        "docker.elastic.co/mcp/elasticsearch",
        "stdio",
    ],
    env={"ES_URL": "http://host.docker.internal:9200"},
)

# # 2. SSE Server:
# server_params = {
#     "url": "http://localhost:8000/sse",
#     "transport": "sse"
# }

# # 3. Streamable HTTP Server:
# server_params = {
#     "url": "http://localhost:8001/mcp",
#     "transport": "streamable-http"
# }

# Example usage (uncomment and adapt once server_params is set):
with MCPServerAdapter(server_params, connect_timeout=60) as mcp_tools:
    print(f"Available tools: {[tool.name for tool in mcp_tools]}")

    elastic_agent = Agent(
        role="Elastic Agent",
        goal="Utilize tools from Elastic Search to asnwer user query.",
        backstory="I can connect to Elastic MCP servers and use their tools to answer {question}.",
        tools=mcp_tools,  # Pass the loaded tools to your agent
        llm=llm,
        reasoning=False,
        verbose=True,
        max_iter=4
    )

    task = Task(
        agent=elastic_agent,
        name="Elastic MCP Task",
        description="""Step 1: Plan the elastic tool calls from the user's query `{question}`.
        Step 2: Use the tools with proper arguments to get the results.
        Step 3: Use the results to answer the user's query.
        One sample entry for reference of index, and other key fields, 
         ```json
            {
            "_index": "logs-aiops_demo",
            "_id": "MOOwHZkBZ-BSO-yHpIDR",
            "_score": 1,
            "_source": {
            "log_level": "INFO",
            "message": "Request to /inventory/items completed in 470ms",
            "customer_name": "Omega Retail",
            "@timestamp": "2025-09-03T19:27:31.471Z",
            "log_type": "lb",
            "environment_name": "dev",
            "application_name": "inventory-service",
            "customer": "cust005"
            }
        ```
        """,
        # description="Answer user's query {question} by querying the Elastic Search using tools. "
        # "To use `search` tool provide the argument as elastic search query DSL."
        # "User index name = `logs-aiops_demo` ",
        expected_output="Answer to the user's query in proper format.",
        markdown= True
    )

    crew = Crew(
        agents=[elastic_agent], tasks=[task], process=Process.sequential, verbose=True
    )

    while True:
        user_input = input("User ('q' to quit): ")
        if user_input == "q":
            break
        answer = crew.kickoff(
            inputs={"question": f"{user_input}. elastic index is 'logs-aiops_demo'"}
        )
        print(answer)
