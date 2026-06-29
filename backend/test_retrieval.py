# backend/test_retrieval.py
from app.retrieval.retriever import retrieve

def test_retrieval():
    query = "What is Apple's total net sales?"
    print(f"Searching for: '{query}'\n")
    
    results = retrieve(query, top_k=3)
    
    for i, chunk in enumerate(results):
        print(f"--- Result {i+1} (Section: {chunk['section_heading']}) ---")
        # Print just the first 150 characters of the chunk to keep it readable
        print(chunk['content'][:150] + "...\n")

if __name__ == "__main__":
    test_retrieval()