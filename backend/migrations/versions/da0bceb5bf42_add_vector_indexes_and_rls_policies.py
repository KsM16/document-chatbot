"""add vector indexes and rls policies

Revision ID: da0bceb5bf42
Revises: 340c775da208
Create Date: 2026-06-29 15:08:07.533774

"""# backend/migrations/versions/xxxx_add_vector_indexes_and_rls_policies.py
"""add vector indexes and rls policies

Revision ID: [Alembic will fill this]
Revises: 340c775da208
Create Date: [Alembic will fill this]
"""
from typing import Sequence, Union
from alembic import op

revision: str = '[Alembic will fill this]'
down_revision: Union[str, None] = '340c775da208'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. HNSW index for fast semantic vector search (Cosine similarity)
    op.execute(
        "CREATE INDEX IF NOT EXISTS document_chunks_embedding_idx "
        "ON document_chunks USING hnsw (embedding vector_cosine_ops);"
    )
    
    # 2. GIN index for fast full-text search (tsvector)
    op.execute(
        "CREATE INDEX IF NOT EXISTS document_chunks_search_vector_idx "
        "ON document_chunks USING gin (search_vector);"
    )

    # 3. Enable Row Level Security on user data tables
    op.execute("ALTER TABLE chat_threads ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;")

    # 4. RLS Policies for chat_threads
    op.execute(
        "CREATE POLICY \"Users can view own threads\" ON chat_threads "
        "FOR SELECT USING (auth.uid() = user_id);"
    )
    op.execute(
        "CREATE POLICY \"Users can insert own threads\" ON chat_threads "
        "FOR INSERT WITH CHECK (auth.uid() = user_id);"
    )

    # 5. RLS Policies for chat_messages
    op.execute(
        "CREATE POLICY \"Users can view own messages\" ON chat_messages "
        "FOR SELECT USING (thread_id IN (SELECT id FROM chat_threads WHERE user_id = auth.uid()));"
    )
    op.execute(
        "CREATE POLICY \"Users can insert own messages\" ON chat_messages "
        "FOR INSERT WITH CHECK (thread_id IN (SELECT id FROM chat_threads WHERE user_id = auth.uid()));"
    )


def downgrade() -> None:
    # Drop policies
    op.execute("DROP POLICY IF EXISTS \"Users can view own messages\" ON chat_messages;")
    op.execute("DROP POLICY IF EXISTS \"Users can insert own messages\" ON chat_messages;")
    op.execute("DROP POLICY IF EXISTS \"Users can view own threads\" ON chat_threads;")
    op.execute("DROP POLICY IF EXISTS \"Users can insert own threads\" ON chat_threads;")
    
    # Disable RLS
    op.execute("ALTER TABLE chat_messages DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE chat_threads DISABLE ROW LEVEL SECURITY;")
    
    # Drop indexes
    op.execute("DROP INDEX IF EXISTS document_chunks_search_vector_idx;")
    op.execute("DROP INDEX IF EXISTS document_chunks_embedding_idx;")