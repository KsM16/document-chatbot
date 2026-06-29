"""add auth trigger for users table

Revision ID: f11743f44fb5
Revises: [Alembic will fill this]
Create Date: 2026-06-29 18:27:53.579172

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f11743f44fb5'
down_revision: Union[str, Sequence[str], None] = '[Alembic will fill this]'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create a function that inserts the new user into the public 'users' table
    op.execute("""
        CREATE OR REPLACE FUNCTION public.handle_new_user()
        RETURNS TRIGGER AS $$
        BEGIN
            INSERT INTO public.users (id, email)
            VALUES (NEW.id, NEW.email);
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql SECURITY DEFINER;
    """)
    
    # 2. Create a trigger that fires this function every time a new user is added to auth.users
    op.execute("""
        CREATE TRIGGER on_auth_user_created
        AFTER INSERT ON auth.users
        FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
    """)

def downgrade() -> None:
    # Clean up if we ever need to rollback
    op.execute("DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;")
    op.execute("DROP FUNCTION IF EXISTS public.handle_new_user();")
