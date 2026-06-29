# backend/app/chat/messages.py
from pydantic import BaseModel

# The AI SDK sends messages as an array of "parts"
class UIMessagePart(BaseModel):
    type: str
    text: str

class UIMessage(BaseModel):
    id: str
    role: str
    parts: list[UIMessagePart]

# The AI SDK sends the thread ID as "id" at the root level
class StreamRequest(BaseModel):
    id: str  # This is the threadId
    messages: list[UIMessage]
    trigger: str | None = None