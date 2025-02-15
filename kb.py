from elasticsearch import Elasticsearch

from settings import ELASTIC_API_KEY, ELASTIC_HOST


def connect_elasticsearch():
    """Connects to the ElasticSearch."""
    es = Elasticsearch(ELASTIC_HOST, api_key=ELASTIC_API_KEY)

    # Check connection
    if es.ping():
        print("Connected to ElasticSearch")
    else:
        print("Failed to connect")
        raise ConnectionError("Failed to connect to ElasticSearch")
    
    return es


def insert_data(es, index, texts, embeddings):
    """Inserts data into the ElasticSearch index."""
    for i, (text, embedding) in enumerate(zip(texts, embeddings)):
        doc = {"text": text, "embedding": embedding.tolist()}
        es.index(index=index, id=i, body=doc)


def search(query, es, index, model, top_k=5):
    """
    Searches for similar documents to the given query in the ElasticSearch index.
    """
    # Convert query into an embedding
    query_embedding = model.encode(query, convert_to_numpy=True, normalize_embeddings=True).tolist()

    # Perform ANN search
    search_body = {
        "size": top_k,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": query_embedding}
                }
            }
        }
    }

    # Execute the search
    response = es.search(index=index, body=search_body)

    # Extract and return results
    return [(hit["_source"]["text"], hit["_score"]) for hit in response["hits"]["hits"]]
