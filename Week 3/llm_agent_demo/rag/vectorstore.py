import chromadb
from rag.embedder import embed_text

client = chromadb.Client()
collection = client.get_or_create_collection("incident_notes")

def add_incident_to_vectorstore(text, metadata):
    embedding = embed_text(text)
    collection.add(documents=[text], embeddings=[embedding], metadatas=[metadata], ids=[metadata["id"]])

def query_vectorstore(query_text):
    embedding = embed_text(query_text)
    results = collection.query(query_embeddings=[embedding], n_results=1)
    return results
