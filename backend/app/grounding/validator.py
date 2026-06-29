# backend/app/grounding/validator.py
from app.assistant.outputs import GroundedAnswer

def validate_grounding(answer: GroundedAnswer, retrieved_chunks: list[dict]) -> bool:
    """
    Validates that every citation in the answer maps to a retrieved chunk.
    Returns True if valid, raises ValueError if invalid.
    """
    # FIX: The key from the database is "id", not "chunk_id"
    retrieved_ids = {str(chunk["id"]) for chunk in retrieved_chunks}
    
    for citation in answer.citations:
        # Ensure we are comparing strings
        if str(citation.chunk_id) not in retrieved_ids:
            raise ValueError(
                f"Citation {citation.chunk_id} does not map to a retrieved passage. "
                f"Retrieved IDs: {retrieved_ids}"
            )
    
    return True