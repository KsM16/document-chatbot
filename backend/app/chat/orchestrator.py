# backend/app/chat/orchestrator.py
import json
from app.assistant.agent import agent
from app.assistant.deps import DocumentAgentDeps
from app.assistant.outputs import GroundedAnswer
from app.retrieval.retriever import retrieve
from app.grounding.validator import validate_grounding
from app.database.supabase import supabase_service_role

async def run_chat_turn(thread_id: str, user_id: str, user_message: str) -> dict:
    """
    Runs one complete chat turn:
    1. Retrieve relevant chunks
    2. Run the agent
    3. Validate grounding
    4. Persist to database
    5. Return the answer with citations
    """
    # 1. Retrieve relevant chunks
    retrieved_chunks = retrieve(user_message, top_k=10)
    
    # 2. Create agent dependencies
    deps = DocumentAgentDeps(
        user_id=user_id,
        thread_id=thread_id,
        retriever=retrieve,
    )
    
    # 3. Run the agent
    result = await agent.run(
        user_message,
        deps=deps,
    )
    
    # 4. Validate grounding
    try:
        validate_grounding(result.output, retrieved_chunks)
    except ValueError as e:
        # If validation fails, return a controlled error
        return {
            "answer": "I cannot answer this question with confidence. The retrieved evidence is insufficient.",
            "citations": [],
            "error": str(e),
        }
    
    # 5. Persist to database (we'll add this in the streaming endpoint)
    return {
        "answer": result.output.answer,
        "citations": [c.model_dump() for c in result.output.citations],
        "retrieved_chunks": retrieved_chunks,
    }