from elasticsearch import Elasticsearch, helpers
from sentence_transformers import SentenceTransformer

ES_URL = "http://localhost:9200"
OLD_INDEX = "logs-aiops_demo"
NEW_INDEX = "logs-aiops_demo_semantic"
BATCH = 200

es = Elasticsearch(ES_URL)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")  # 384 dims

def scan_old_index(index):
    for hit in helpers.scan(
        es, 
        index=index, 
        _source=["message","@timestamp","application_name",
                 "customer","customer_name","environment_name",
                 "log_level","log_type"]
    ):
        yield hit

def bulk_index_with_vectors(old_index, new_index):
    actions = []
    for count, doc in enumerate(scan_old_index(old_index), 1):
        src = doc["_source"]
        # print("\n=====src======", src, end="\t")
        message = src.get("message", "") or ""
        vec = model.encode(message).tolist()

        new_doc = {
            "message": message,
            "@timestamp": src.get("@timestamp"),
            "application_name": src.get("application_name"),
            "customer": src.get("customer"),
            "customer_name": src.get("customer_name"),
            "environment_name": src.get("environment_name"),
            "log_level": src.get("log_level"),
            "log_type": src.get("log_type"),
            "message_vector": vec
        }

        actions.append({
            "_op_type": "index",
            "_index": new_index,
            "_id": doc["_id"],
            "_source": new_doc
        })

        if len(actions) >= BATCH:
            print(f"Indexing {count} documents...")
            try:
                helpers.bulk(es, actions)
            except helpers.BulkIndexError as e:
                print(f"Error idexing documents: {e}")
                for error in e.errors:
                    print(f"Error for document {error}")
            actions = []
        
    if len(actions) > 0:
        print(f"Indexing {count} documents...")
        try:
            helpers.bulk(es, actions)
        except helpers.BulkIndexError as e:
            print(f"Error indexing documents: {e}")
            for error in e.errors:
                print(f"Error for document {error}")

if __name__ == "__main__":
    bulk_index_with_vectors(OLD_INDEX, NEW_INDEX)
    print("✅ Reindex complete")
