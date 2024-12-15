import os
from dotenv import load_dotenv
from groq import Groq
from recall import recall_documents
from filter import filter_documents
from prompt_generator import generate_prompt

load_dotenv()
api_key = os.getenv("API_KEY")

client = Groq(api_key=api_key)

def main(query, documents):
    recalled_docs = recall_documents(query, documents)
    filtered_docs = filter_documents(query, recalled_docs)
    prompt = generate_prompt(query, filtered_docs)
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    
    print(chat_completion.choices[0].message.content)

if __name__ == "__main__":
    sample_documents = [
        "This is a sample document about AI.",
        "Another document discussing the importance of fast language models.",
        "This document is not relevant to the query.",
    ]
    main("Explain the importance of fast language models", sample_documents)