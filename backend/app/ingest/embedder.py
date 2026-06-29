# backend/app/ingest/embedder.py
import time
from google import genai
from app.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def get_embedding(text: str) -> list[float]:
    """
    Generates a 1536-dimensional embedding for the given text using Gemini.
    """
    text_to_embed = text[:8000]
    
    time.sleep(0.5)  # Rate limiting
    
    try:
        response = client.models.embed_content(
            model=settings.GEMINI_EMBEDDING_MODEL,
            contents=[text_to_embed],
            config={"output_dimensionality": 1536}  # Force 1536 dimensions
        )
        return response.embeddings[0].values
    except Exception as e:
        if "429" in str(e):
            print(f"    Rate limit hit, waiting 60 seconds...")
            time.sleep(60)
            response = client.models.embed_content(
                model=settings.GEMINI_EMBEDDING_MODEL,
                contents=[text_to_embed],
                config={"output_dimensionality": 1536}
            )
            return response.embeddings[0].values
        raise