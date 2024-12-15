def filter_documents(query, documents, threshold=0.5):
    def char_similarity(str1, str2):
        return len(set(str1) & set(str2)) / len(set(str1) | set(str2))
    
    filtered_docs = [doc for doc in documents if char_similarity(query, doc) > threshold]
    
    return filtered_docs