# backend/app/ingest/chunker.py
import re

def chunk_markdown(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[dict]:
    """
    Splits Markdown text into chunks. 
    Returns a list of dicts with 'chunk_index', 'content', and 'section_heading'.
    """
    # Split by double newlines (paragraphs)
    paragraphs = re.split(r'\n\n+', text)
    
    chunks = []
    current_chunk_lines = []
    current_length = 0
    chunk_index = 0
    current_heading = "Introduction"

    for para in paragraphs:
        # Check if this paragraph is a heading (starts with #)
        if para.startswith("#"):
            current_heading = para.replace("#", "").strip()
            continue # Don't add the heading itself as a separate chunk, it attaches to the next one

        if current_length + len(para) > chunk_size and current_chunk_lines:
            # Save the current chunk
            chunks.append({
                "chunk_index": chunk_index,
                "section_heading": current_heading,
                "content": "\n\n".join(current_chunk_lines),
            })
            
            # Handle overlap (keep the last paragraph for context)
            overlap_lines = current_chunk_lines[-1:] if current_chunk_lines else []
            current_chunk_lines = overlap_lines + [para]
            current_length = sum(len(line) for line in current_chunk_lines)
            chunk_index += 1
        else:
            current_chunk_lines.append(para)
            current_length += len(para)

    # Don't forget the last chunk
    if current_chunk_lines:
        chunks.append({
            "chunk_index": chunk_index,
            "section_heading": current_heading,
            "content": "\n\n".join(current_chunk_lines),
        })

    return chunks