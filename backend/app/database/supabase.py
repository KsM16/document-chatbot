# backend/app/database/supabase.py
from supabase import Client, create_client

from app.config import settings

# =====================================================================
# 1. Service Role Client (Bypasses Row Level Security)
# =====================================================================
# Use this for backend-only tasks: ingesting documents, reading all 
# source chunks, or administrative tasks. It has full database access.
supabase_service_role: Client = create_client(
    settings.SUPABASE_URL, 
    settings.SUPABASE_SERVICE_ROLE_KEY
)

# =====================================================================
# 2. User-Scoped Client Factory (Enforces Row Level Security)
# =====================================================================
# Use this when handling actual user requests (e.g., saving a chat).
# It uses the user's JWT to ensure they can ONLY access their own data.
def get_user_scoped_client(user_token: str) -> Client:
    """
    Returns a Supabase client scoped to a specific user's JWT.
    """
    return create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_ANON_KEY,
        options={
            "headers": {
                "Authorization": f"Bearer {user_token}"
            }
        }
    )