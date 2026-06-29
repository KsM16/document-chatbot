# backend/app/api/chat.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import asyncio

from app.auth.dependencies import get_current_user
from app.database import chats
from app.chat.messages import StreamRequest
from app.chat.streaming import format_text_delta, format_error, format_finish
from app.chat.orchestrator import run_chat_turn


router = APIRouter()

@router.get("/threads")
def list_threads(current_user: dict = Depends(get_current_user)):
    return chats.list_threads(current_user["id"])

@router.post("/threads")
def create_thread(current_user: dict = Depends(get_current_user)):
    return chats.create_thread(current_user["id"])

@router.get("/threads/{thread_id}")
def get_thread(thread_id: str, current_user: dict = Depends(get_current_user)):
    thread = chats.get_thread(thread_id, current_user["id"])
    if not thread:
        # Returns 403 if it exists but belongs to someone else, 404 if it doesn't exist
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread

@router.get("/threads/{thread_id}/messages")
def get_messages(thread_id: str, current_user: dict = Depends(get_current_user)):
    thread = chats.get_thread(thread_id, current_user["id"])
    if not thread:
        raise HTTPException(status_code=403, detail="Forbidden")
    return chats.get_messages(thread_id)



@router.post("/chat/stream")
async def stream_chat(
    request: StreamRequest, 
    current_user: dict = Depends(get_current_user)
):
    # 1. Verify ownership
    thread = chats.get_thread(request.id, current_user["id"])
    if not thread:
        raise HTTPException(status_code=403, detail="Forbidden")
        
    # 2. Extract the user message
    user_msg = request.messages[-1]
    user_content = "".join(part.text for part in user_msg.parts if part.type == "text")
    
    # 3. Save the user message
    chats.save_message(request.id, "user", user_content)

    # 4. Stream the agent response
    async def generate():
        try:
            # Run the orchestrator
            result = await run_chat_turn(
                thread_id=request.id,
                user_id=current_user["id"],
                user_message=user_content,
            )
            
            # Stream the answer character by character
            for char in result["answer"]:
                yield format_text_delta(char)
                await asyncio.sleep(0.01)  # Simulate streaming
            
            # Save the assistant message
            chats.save_message(request.id, "assistant", result["answer"])
            
            # TODO: Save citations to message_citations table (we'll add this next)
            
            yield format_finish()
            
        except Exception as e:
            yield format_error(str(e))

    return StreamingResponse(
        generate(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )