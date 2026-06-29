# backend/app/database/models/source_document.py
import uuid
from datetime import datetime, date
from sqlalchemy import String, DateTime, Date, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .document_chunk import DocumentChunk
    
from .base import Base

class SourceDocument(Base):
    __tablename__ = "source_documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticker: Mapped[str] = mapped_column(String(10), nullable=False, index=True) # e.g., AAPL
    form_type: Mapped[str] = mapped_column(String(20), nullable=False)         # e.g., 10-K
    filing_date: Mapped[date] = mapped_column(Date, nullable=False)
    report_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    accession_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    source_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    local_path: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    chunks: Mapped[list["DocumentChunk"]] = relationship(back_populates="source_document", cascade="all, delete-orphan")