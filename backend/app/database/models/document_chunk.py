# backend/app/database/models/document_chunk.py
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Integer, Text, ForeignKey, func, Computed
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .message_citation import MessageCitation
    from .source_document import SourceDocument

from .base import Base
from app.config import settings

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("source_documents.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    page_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    section_heading: Mapped[str | None] = mapped_column(String(512), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # 1536 dimensions for Gemini gemini-embedding-2
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(settings.GEMINI_EMBEDDING_DIMENSIONS), 
        nullable=True
    )
    
    # GENERATED tsvector column for full-text search.
    # Postgres will automatically update this whenever 'content' changes!
    search_vector: Mapped[str | None] = mapped_column(
        TSVECTOR,
        Computed("to_tsvector('english', coalesce(content, ''))", persisted=True),
        nullable=True
    )
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    source_document: Mapped["SourceDocument"] = relationship(back_populates="chunks")
    citations: Mapped[list["MessageCitation"]] = relationship(back_populates="chunk", cascade="all, delete-orphan")