from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Chroma
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import sentence_transformers

# === Load and Split PDF ===
loader = PyPDFLoader(r"C:\Users\admin\Documents\VP\Week 3\llm_agent_demo\example_data\knowledge_article.pdf")
docs = loader.load()

# === Chunking the document ===
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_documents(docs)

from langchain_community.embeddings import SentenceTransformerEmbeddings

embedding_model = SentenceTransformerEmbeddings()
embeddings = embedding_model.embed_documents([chunk.page_content for chunk in chunks])

persist_directory = r"C:\Users\admin\Documents\VP\Week 3\llm_agent_demo\data\chroma_db"
vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=persist_directory
)

# # === Create Vectorstore ===
# # vectorstore = FAISS.from_documents(chunks, embeddings)
# # === Save Vectorstore to disk ===
# vectorstore.save_local(r"C:\Users\admin\Documents\VP\Week 3\llm_agent_demo\data/rag_vectorstore", index_name="faiss_index")

print("✅ Vectorstore created and saved to 'data/rag_vectorstore'")
