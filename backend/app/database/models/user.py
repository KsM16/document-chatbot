# backend/app/database/models/user.py
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .chat_thread import ChatThread

from .base import Base

class User(Base):
    __tablename__ = "users"

    # Primary key matches the Supabase Auth UUID
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    threads: Mapped[list["ChatThread"]] = relationship(back_populates="user", cascade="all, delete-orphan")