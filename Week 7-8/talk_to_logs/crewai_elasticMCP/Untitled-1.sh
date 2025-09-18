curl -XGET 'localhost:9200/logs-aiops_demo/_search' -H 'Content-Type: application/json' -d '
{
  "size": 0,
  "aggs": {
    "unique_log_type": {
      "terms": {
        "field": "log_type.keyword",
        "size": 100
      }
    }
  }
}
'

curl -XGET 'localhost:9200/logs-aiops_demo/_search' -H 'Content-Type: application/json' -d '
{
  "size": 0,
  "aggs": {
    "unique_log_type": {
      "cardinality": {
        "field": "log_type"
      }
    }
  }
}
'

curl -XGET 'localhost:9200/logs-aiops_demo/_search' -H 'Content-Type: application/json' -d '
{
  "query": {
    "match": {
      "log_type.keyword": "*"
    }
  }
}
'

curl -XGET 'localhost:9200/logs-aiops_demo/_search' -H 'Content-Type: application/json' -d '
{
  "size": 0,
  "aggs": {
    "unique_cn": {
      "terms": {
        "field": "customer_name",
        "size": 100
      }
    }
  }
}
'

curl -XPUT 'localhost:9200/logs-aiops_demo/_mapping' -H 'Content-Type: application/json' -d '
{
  "properties": {
    "log_type": {
      "type": "keyword",
      "fielddata": true
    }
  }
}
'

curl -XGET 'localhost:9200/logs-aiops_demo/_search' -H 'Content-Type: application/json' -d '
{
    "query": {
        "bool": {
            "filter": [
                {
                    "term": {
                        "log_level": "WARN"
                    }
                },
                {
                    "term": {
                        "log_type": "lb"
                    }
                },
                {
                    "term": {
                        "environment_name": "dev"
                    }
                },
                {
                    "term": {
                        "application_name": "inventory-service"
                    }
                }
            ]
        }
    },
    "from": 0,
    "size": 100
}
'

curl -X DELETE "localhost:9200/logs-aiops_demo_semantic"

curl -X PUT "http://localhost:9200/logs-aiops_demo_semantic" -H "Content-Type: application/json" -d '
{
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "@timestamp": { "type": "date" },
      "application_name": { "type": "keyword" },
      "customer": { "type": "keyword" },
      "customer_name": { "type": "text" },
      "environment_name": { "type": "keyword" },
      "log_level": { "type": "keyword" },
      "log_type": { "type": "keyword" },
      "message": { "type": "text" },
      "message_vector": {
        "type": "dense_vector",
        "dims": 384,
        "index": true,
        "similarity": "cosine"
      }
    }
  }
}
'