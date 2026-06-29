# backend/app/database/chats.py
import uuid
from datetime import datetime, timezone
from app.database.supabase import supabase_service_role

def create_thread(user_id: str, title: str | None = None) -> dict:
    response = supabase_service_role.table("chat_threads").insert({
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "title": title or "New Chat",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }).execute()
    return response.data[0]

def list_threads(user_id: str) -> list[dict]:
    response = supabase_service_role.table("chat_threads") \
        .select("id, title, created_at, updated_at") \
        .eq("user_id", user_id) \
        .order("updated_at", desc=True) \
        .execute()
    return response.data

def get_thread(thread_id: str, user_id: str) -> dict | None:
    response = supabase_service_role.table("chat_threads") \
        .select("*") \
        .eq("id", thread_id) \
        .eq("user_id", user_id) \
        .execute()
    return response.data[0] if response.data else None

def get_messages(thread_id: str) -> list[dict]:
    response = supabase_service_role.table("chat_messages") \
        .select("id, role, content, created_at") \
        .eq("thread_id", thread_id) \
        .order("created_at") \
        .execute()
    return response.data

def save_message(thread_id: str, role: str, content: str) -> dict:
    response = supabase_service_role.table("chat_messages").insert({
        "id": str(uuid.uuid4()),
        "thread_id": thread_id,
        "role": role,
        "content": content,
        "created_at": datetime.now(timezone.utc).isoformat()
    }).execute()
    return response.data[0]