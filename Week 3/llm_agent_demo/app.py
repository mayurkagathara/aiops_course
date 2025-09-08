from langchain import hub
from langchain.agents import initialize_agent, Tool
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

import pandas as pd
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# === Load Ollama Local Model ===
llm = Ollama(model="qwen2.5:1.5b")

# === Tool 1: RAG over VectorStore ===
def load_rag_tool():
    # Initialize the embedding model
    cache_dir = os.getenv("SENTENCE_TRANSFORMERS_HOME", "data/embedding_cache")

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
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
        return_source_documents=True
    )
    
    def rag_tool_func(query: str) -> str:
        result = qa_chain({"query": query})
        answer = result["result"]
        sources = [doc.metadata.get("source", "N/A") for doc in result["source_documents"]]
        return f"{answer}\n\n[Sourced from: {', '.join(set(sources))}]"

    return Tool(
        name="IncidentRAGTool",
        func=rag_tool_func,
        description="Use this to answer questions about incident root causes and resolutions based on past incidents."
    )

# === Tool 2: CSV Lookup ===
def load_automation_tool():
    df = pd.read_csv("data/automations.csv")

    def automation_lookup(query: str) -> str:
        query_lower = query.lower()
        matches = df[df.apply(lambda row: query_lower in row["Automation Name"].lower() 
                              or query_lower in row["Description"].lower(), axis=1)]
        if matches.empty:
            return "No automation found matching your query."
        return "\n\n".join([
            f"[{row['Automation ID']}] {row['Automation Name']}: {row['Description']}"
            for _, row in matches.iterrows()
        ])

    return Tool(
        name="AutomationSearchTool",
        func=automation_lookup,
        description="Use this to search for available automation tools and automatino runbook related to the query problem."
    )

# === define the prompt ===
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI assistant. You have access to the following tools: {tools}. "
        "Do not ask the followup question to user, first look at the tools. "
        "Try to answer the question using tools and if not possible, try to answer generally"),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

# === Initialize Agent ===
tools = [load_rag_tool(), load_automation_tool()]

prompt = hub.pull("rlm/rag-prompt")

agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True,
    prompt = prompt
)

# === Command Line Chat Loop ===
if __name__ == "__main__":
    print("🤖 AIOps LLM Agent is ready! Type your query or 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            break
        try:
            response = agent.invoke({"input":user_input})
            print("Agent:", response["output"])
        except Exception as e:
            print("Error:", str(e), '\nTry Again...')
            continue
