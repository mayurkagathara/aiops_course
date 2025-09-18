# %%
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

es = Elasticsearch("http://localhost:9200")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# %%
query = "UI is running very slow, find me root cause"
vec = model.encode(query).tolist()

body = {
    "size": 20,
    "query": {
        "knn": {
            "field": "message_vector",
            "query_vector": vec,
            "num_candidates": 100,
            "filter": {"bool": {"must": [{"term": {"customer": "cust001"}}]}},
        }
    },
    "_source": ["message", "application_name", "customer", "@timestamp"],
}

res = es.search(index="logs-aiops_demo_semantic", body=body)
for hit in res["hits"]["hits"]:
    print(
        hit["_score"],
        hit["_source"]["message"],
        hit["_source"]["application_name"],
        hit["_source"]["customer"],
        hit["_source"]["@timestamp"],
    )


# %%

# body = {
#     "size": 5,
#     "query": {
#         "script_score": {
#             "query": {"match_all": {}},
#             "script": {
#                 "source": ("cosineSimilarity(params.query_vector, 'message_vector') + 1.0) / 2",
#                 "params": {"query_vector": vec}
#             }
#         }
#     },
#     "_source": ["message", "application_name", "customer", "@timestamp"]
# }

# Working

# body = {
#     "knn": {
#         "field": "message_vector",
#         "query_vector": vec,
#         "k": 5,
#         "num_candidates": 100
#     },
#     "_source": ["message","application_name","customer","@timestamp"]
# }
