# backend/app/chat/streaming.py
import json

def format_text_delta(text: str) -> str:
    # Vercel AI SDK Data Stream Protocol for text
    return f'0:"{text}"\n'

def format_error(error: str) -> str:
    return f'e:{json.dumps({"error": error})}\n'

def format_finish() -> str:
    return f'd:{json.dumps({"finishReason": "stop"})}\n'