from typing import Annotated, Optional

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_ollama import ChatOllama
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

from langchain_core.tools import tool
import os
import random
import pandas as pd

from langgraph.checkpoint.memory import InMemorySaver
memory = InMemorySaver()

# === Tool 1: RAG over VectorStore ===
# This tool uses a pre-built Chroma DB to answer questions about past incidents.
# The @tool decorator from langchain_core simplifies tool creation.
@tool
def IncidentRAGTool(query: str) -> str:
    """Use this to answer questions about incident root causes and resolutions based on past incidents.
    For any IT related problem, root cause and resolutions are provided by this tool."""
    cache_dir = os.getenv("SENTENCE_TRANSFORMERS_HOME", "data/embedding_cache")
    # Initialize the embedding model
    embedding_model = SentenceTransformerEmbeddings(
        # model_name="all-MiniLM-L6-v2", 
        cache_folder = cache_dir
    )

    # Load the persisted vector store
    persist_directory = "data/chroma_db"
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model
    )
    
    # Create a RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOllama(model="qwen2.5:1.5b"),
        retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
        return_source_documents=True
    )
    
    result = qa_chain({"query": query})
    answer = result["result"]
    sources = [doc.metadata.get("source", "N/A") for doc in result["source_documents"]]
    return f"{answer}\n\n[Sourced from: {', '.join(set(sources))}]"

# === Tool 2: CSV Lookup ===
# This tool searches a CSV file for automation scripts.
@tool
def AutomationSearchTool(query: str) -> str:
    """Use this to search for available automation tools related to the query problem."""
    
    df = pd.read_csv("data/automations.csv")
    query_lower_set = set(query.lower().split())
    matches = df[df.apply(lambda row: bool(query_lower_set & set(row["Automation Name"].lower().split()))
                          or bool(query_lower_set & set(row["Description"].lower().split())), axis=1)]
    if matches.empty:
        return "No automation found matching your query."
    return "\n\n".join([
        f"[{row['Automation ID']}] {row['Automation Name']}: {row['Description']}"
        for _, row in matches.iterrows()
    ])

# Load the defined tools. LangGraph expects them in a list.
tools = [IncidentRAGTool, AutomationSearchTool]

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]
    tool_output: str

model_name = "qwen2.5:1.5b"
llm_with_tools = ChatOllama(model=model_name, base_url="http://localhost:11434").bind_tools(tools = tools)

from langchain.prompts import ChatPromptTemplate

# For a chat model
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Always try to use the tools. Do not ask follow up questions to user. "
    "If you do not find answer from tools, inform user about it. Do not answer genrally "),
    ("user", "{user_input}")
])

def chatbot(state: State):
    prompt_with_input = chat_prompt.invoke({"user_input": state["messages"]})
    return {"messages": [llm_with_tools.invoke(prompt_with_input)]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile(checkpointer=memory)

## OPTIONAL - to save graph image
def save_graph_image(graph):
    from IPython.display import Image # You still need Image for handling the image data
    import os

    # Assuming 'graph' is an object that has a get_graph().draw_mermaid_png() method
    # This method should return the raw PNG image data as bytes.
    png_graph_data = graph.get_graph().draw_mermaid_png()

    # Define the filename to save the image
    output_filename = "mermaid_graph.png"

    # Save the image data to a PNG file
    with open(output_filename, "wb") as f:
        f.write(png_graph_data)

    print(f"Graph saved as '{output_filename}' in {os.getcwd()}")

# save_graph_image(graph)

def stream_graph_updates(user_input: str, config):
    for event in graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
        stream_mode= "values"):
        event["messages"][-1].pretty_print()
        event["messages"]

user_id = "1"
config = {"configurable": {"thread_id": "1"}}
while True:
    if not user_id:
        user_id = input("enter_user_id: ")
        config = {"configurable": {"thread_id": "chat_"+ user_id}}
        print("got user id", user_id )
    try:
        print("taking user input...")
        user_input = input("User: ")
        print("You: " + user_input)
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input, config)
        
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input, config)
        break