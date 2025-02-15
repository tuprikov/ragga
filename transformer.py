"""
This module contains the code for the transformer model.
"""
def get_embeddings(model, data):
    """
    Returns the embeddings for the given data.
    """
    texts = list(data.values())
    return model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
