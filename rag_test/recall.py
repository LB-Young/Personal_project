import numpy as np
from embeddings.embedding_model import generate_embedding

def recall_documents(query, documents):
    query_embedding = generate_embedding(query)
    doc_embeddings = [generate_embedding(doc) for doc in documents]
    
    similarities = [np.dot(query_embedding, doc_embedding) for doc_embedding in doc_embeddings]
    sorted_docs = [doc for _, doc in sorted(zip(similarities, documents), reverse=True)]
    
    return sorted_docs