import streamlit as st
import pandas as pd
import traceback
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer


# Replace with your Elasticsearch connection details
ES_CLIENT_CONFIG = {"hosts": ["http://localhost:9200"]}


def get_distinct_values(index_name: str, fields: list, size: int = 100) -> dict:
    """
    Fetches distinct values from Elasticsearch for a list of fields.

    Parameters
    ----------
    index_name : str
        The name of the Elasticsearch index to query.
    fields : list
        A list of field names to query for distinct values.
    size : int, optional
        The number of top unique values to return for each field. Defaults to 100.

    Returns
    -------
    dict
        A dictionary mapping each field to its top unique values.
    """
    try:
        es = Elasticsearch(**ES_CLIENT_CONFIG)
        # print(es.info(human=True))
        distinct_values = {}
        for field in fields:
            query = {
                "size": 0,
                "aggs": {
                    f"unique_{field}": {"terms": {"field": f"{field}", "size": size}}
                },
            }
            # print(query)
            response = es.search(index=index_name, body=query, allow_no_indices=True)
            # print(response)
            buckets = response["aggregations"][f"unique_{field}"]["buckets"]
            values = [
                bucket["key"] + f"  ({bucket['doc_count']})" for bucket in buckets
            ]
            distinct_values[field] = values
        # print(distinct_values)
        return distinct_values

    except Exception as e:
        print(traceback.format_exc())
        st.error(f"An unexpected error occurred during dropdown data fetch: {e}")
        return {}


def search_documents(
    index_name: str,
    filters: dict,
    page: int,
    page_size: int,
    enable_knn: bool = False,
    knn_results: int = 10,
    user_query: str = "",
) -> tuple:
    """
    Queries Elasticsearch for documents based on selected filters, with pagination.

    Parameters
    ----------
    index_name : str
        The name of the Elasticsearch index.
    filters : dict
        A dictionary of field:value filters.
    page : int
        The current page number (1-indexed).
    page_size : int
        The number of results per page.

    Returns
    -------
    tuple
        A tuple containing a list of hits and the total number of hits.
    """
    try:
        es = Elasticsearch(**ES_CLIENT_CONFIG)

        # Build the Elasticsearch query
        bool_query = {"bool": {"must": []}}
        for field, value in filters.items():
            if value and value != "All":
                if field in ["start_date", "end_date"]:
                    if field == "start_date" and value:
                        bool_query["bool"]["must"].append(
                            {"range": {"@timestamp": {"gte": value}}}
                        )
                    elif field == "end_date" and value:
                        bool_query["bool"]["must"].append(
                            {"range": {"@timestamp": {"lte": value}}}
                        )
                else:
                    bool_query["bool"]["must"].append({"term": {f"{field}": value}})

        # Build the main search request body
        if enable_knn:
            vec = st.session_state.model.encode(user_query).tolist()
            body = {
                "size": knn_results,
                "query": {
                    "knn": {
                        "field": "message_vector",
                        "query_vector": vec,
                        "num_candidates": 100,
                        "filter": bool_query,
                    }
                },
            }
        else:
            body = {
                "query": bool_query,
                "from": (page - 1) * page_size,
                "size": page_size,
            }

        # print("\n\n", str(body))

        # Execute the search
        response = es.search(index=index_name, body=body)
        # print("\n\nresponse ", response)
        hits = [hit["_source"] for hit in response["hits"]["hits"]]
        total_hits = response["hits"]["total"]["value"]

        # print(f"\n\nhits = {hits}, total_hits = {total_hits}")

        return hits, knn_results if enable_knn else total_hits

    except Exception as e:
        st.error(f"An unexpected error occurred during search: {e}")
        return [], 0
