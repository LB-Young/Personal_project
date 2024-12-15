from main import main

if __name__ == "__main__":
    query = input("请输入您的问题：")
    sample_documents = [
        "This is a sample document about AI.",
        "Another document discussing the importance of fast language models.",
        "This document is not relevant to the query.",
    ]
    main(query, sample_documents)