# backend/app/database/models/__init__.py
from .base import Base
from .user import User
from .source_document import SourceDocument
from .document_chunk import DocumentChunk
from .chat_thread import ChatThread
from .chat_message import ChatMessage
from .message_citation import MessageCitation

# Export all models so Alembic can see them when generating migrations
__all__ = [
    "Base",
    "User",
    "SourceDocument",
    "DocumentChunk",
    "ChatThread",
    "ChatMessage",
    "MessageCitation",
]