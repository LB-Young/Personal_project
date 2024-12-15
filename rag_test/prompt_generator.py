def generate_prompt(query, documents):
    prompt = f"User query: {query}\n\nRelevant documents:\n"
    for doc in documents:
        prompt += f"- {doc}\n"
    return prompt