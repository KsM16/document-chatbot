# backend/app/retrieval/queries.py
from sqlalchemy import text
from app.database.engine import SessionLocal

def semantic_search(query_embedding: list[float], limit: int = 20) -> list[dict]:
    """
    Finds chunks with similar meaning using pgvector cosine distance.
    """
    with SessionLocal() as db:
        # We cast the list to a vector type in Postgres
        query = text("""
            SELECT id, content, section_heading, source_document_id,
                   1 - (embedding <=> CAST(:embedding AS vector)) AS similarity
            FROM document_chunks
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT :limit
        """)
        result = db.execute(query, {"embedding": str(query_embedding), "limit": limit})
        return [dict(row._mapping) for row in result]

def fulltext_search(query_text: str, limit: int = 20) -> list[dict]:
    """
    Finds chunks containing exact keywords using Postgres tsvector.
    """
    with SessionLocal() as db:
        query = text("""
            SELECT id, content, section_heading, source_document_id,
                   ts_rank(search_vector, plainto_tsquery('english', :query)) AS rank
            FROM document_chunks
            WHERE search_vector @@ plainto_tsquery('english', :query)
            ORDER BY rank DESC
            LIMIT :limit
        """)
        result = db.execute(query, {"query": query_text, "limit": limit})
        return [dict(row._mapping) for row in result]