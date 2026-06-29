# backend/app/retrieval/retriever.py
from app.ingest.embedder import get_embedding
from .queries import semantic_search, fulltext_search
from .fusion import reciprocal_rank_fusion

def retrieve(query: str, top_k: int = 5) -> list[dict]:
    """
    Main entry point for retrieval.
    1. Embeds the query.
    2. Runs semantic and full-text search.
    3. Fuses the results.
    4. Returns the top K chunks.
    """
    # 1. Generate embedding for the user's question
    query_embedding = get_embedding(query)
    
    # 2. Run both searches (fetching top 20 for fusion)
    semantic_results = semantic_search(query_embedding, limit=20)
    fulltext_results = fulltext_search(query, limit=20)
    
    # 3. Fuse the results
    fused_results = reciprocal_rank_fusion([semantic_results, fulltext_results])
    
    # 4. Return only the top K results
    return fused_results[:top_k]