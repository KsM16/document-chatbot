# backend/app/assistant/outputs.py
from pydantic import BaseModel, Field

class Citation(BaseModel):
    """A citation to a specific chunk of a document."""
    chunk_id: str
    quote_snippet: str = Field(description="The exact text from the chunk that supports the answer")

class GroundedAnswer(BaseModel):
    """
    The agent's output: an answer with citations.
    """
    answer: str = Field(description="The grounded answer to the user's question")
    citations: list[Citation] = Field(description="List of citations supporting the answer")