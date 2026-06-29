# backend/app/assistant/agent.py
from pathlib import Path
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from .deps import DocumentAgentDeps
from .outputs import GroundedAnswer
from app.config import settings

# Load the instructions from the markdown file
INSTRUCTIONS_PATH = Path(__file__).parent / "instructions.md"
INSTRUCTIONS = INSTRUCTIONS_PATH.read_text()

# Create the Google provider with your API key
provider = GoogleProvider(api_key=settings.GEMINI_API_KEY)

# 🛠️ FIXED: Updated to a currently supported model version
model = GoogleModel("gemini-2.5-flash", provider=provider)

# Create the agent
agent = Agent(
    model,
    deps_type=DocumentAgentDeps,
    output_type=GroundedAnswer,
    system_prompt=INSTRUCTIONS,
)

# Define tools the agent can use
@agent.tool
def search_filings(ctx: RunContext[DocumentAgentDeps], query: str) -> list[dict]:
    """
    Search the SEC filing corpus for relevant passages.
    Returns a list of chunks with their content and metadata.
    """
    results = ctx.deps.retriever(query, top_k=10)
    return [
        {
            "chunk_id": r["id"],
            "content": r["content"],
            "section_heading": r["section_heading"],
        }
        for r in results
    ]

@agent.tool
def read_chunk(ctx: RunContext[DocumentAgentDeps], chunk_id: str) -> dict:
    """
    Read the full content of a specific chunk by its ID.
    """
    from app.database.engine import SessionLocal
    from sqlalchemy import text
    
    with SessionLocal() as db:
        query = text("""
            SELECT id, content, section_heading, source_document_id
            FROM document_chunks
            WHERE id = :chunk_id
        """)
        result = db.execute(query, {"chunk_id": chunk_id}).first()
        if result:
            return {
                "chunk_id": result[0],
                "content": result[1],
                "section_heading": result[2],
            }
        return {"error": "Chunk not found"}





# # backend/app/assistant/agent.py
# from pathlib import Path
# from pydantic_ai import Agent, RunContext
# from pydantic_ai.models.google import GoogleModel
# from pydantic_ai.providers.google import GoogleProvider
# from .deps import DocumentAgentDeps
# from .outputs import GroundedAnswer
# from app.config import settings

# # Load the instructions from the markdown file
# INSTRUCTIONS_PATH = Path(__file__).parent / "instructions.md"
# INSTRUCTIONS = INSTRUCTIONS_PATH.read_text()

# # Create the Google provider with your API key
# provider = GoogleProvider(api_key=settings.GEMINI_API_KEY)

# model = GoogleModel("gemini-1.5-flash", provider=provider)

# # Create the agent
# agent = Agent(
#     model,
#     deps_type=DocumentAgentDeps,
#     output_type=GroundedAnswer,
#     system_prompt=INSTRUCTIONS,
# )

# # Define tools the agent can use
# @agent.tool
# def search_filings(ctx: RunContext[DocumentAgentDeps], query: str) -> list[dict]:
#     """
#     Search the SEC filing corpus for relevant passages.
#     Returns a list of chunks with their content and metadata.
#     """
#     results = ctx.deps.retriever(query, top_k=10)
#     return [
#         {
#             "chunk_id": r["id"],
#             "content": r["content"],
#             "section_heading": r["section_heading"],
#         }
#         for r in results
#     ]

# @agent.tool
# def read_chunk(ctx: RunContext[DocumentAgentDeps], chunk_id: str) -> dict:
#     """
#     Read the full content of a specific chunk by its ID.
#     """
#     from app.database.engine import SessionLocal
#     from sqlalchemy import text
    
#     with SessionLocal() as db:
#         query = text("""
#             SELECT id, content, section_heading, source_document_id
#             FROM document_chunks
#             WHERE id = :chunk_id
#         """)
#         result = db.execute(query, {"chunk_id": chunk_id}).first()
#         if result:
#             return {
#                 "chunk_id": result[0],
#                 "content": result[1],
#                 "section_heading": result[2],
#             }
#         return {"error": "Chunk not found"}