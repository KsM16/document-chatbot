# backend/app/assistant/deps.py
from dataclasses import dataclass
from app.retrieval.retriever import retrieve

@dataclass
class DocumentAgentDeps:
    """
    Dependencies injected into the PydanticAI agent.
    """
    user_id: str
    thread_id: str
    retriever: callable  # The retrieve function from retrieval/retriever.py