"""
Main module.
"""
from sentence_transformers import SentenceTransformer

from helpers import load_jsonl
from kb import connect_elasticsearch, insert_data, search
from settings import SCRAPED_DATA_FILE, mapping
from transformer import get_embeddings


INDEX_NAME = "leudelange"
model = SentenceTransformer("all-MiniLM-L6-v2")


def process_and_insert_data():
    """
    Load data, process embeddings, and insert into Elasticsearch.
    """
    # Load data from a JSONL file and return its embeddings.
    data = load_jsonl(SCRAPED_DATA_FILE, {})
    # Remove empty values from the data.
    data = {key: value for key, value in data.items() if value}
    embeddings = get_embeddings(model, data)

    es = connect_elasticsearch()
    schema = mapping.copy()
    schema["mappings"]["properties"]["embedding"]["dims"] = len(embeddings[0])

    # Create the index
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, body=schema)
    
    # Insert data into the index
    insert_data(es, INDEX_NAME, list(data.values()), embeddings)


def main():
    """
    Main function.
    """
    query = "Quels sont horaires d'ouverture de la mairie ?"
    es = connect_elasticsearch()
    
    results = search(query, es, INDEX_NAME, model)
    # Display results
    for text, score in results:
        print(f"Score: {score:.4f}\nText: {text}\n{'-'*50}")


if __name__ == "__main__":
    main()
