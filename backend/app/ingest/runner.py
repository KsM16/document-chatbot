# backend/app/ingest/runner.py
import json
import uuid  # Add this import
from pathlib import Path
from app.database.supabase import supabase_service_role
from .parser import parse_sec_html_to_markdown
from .chunker import chunk_markdown
from .embedder import get_embedding

# Path to your local data
DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"
MANIFEST_PATH = DATA_DIR / "downloads" / "manifest.json"

def run_ingestion():
    if not MANIFEST_PATH.exists():
        print("Error: manifest.json not found. Run `uv run data/download.py` first.")
        return

    manifest = json.loads(MANIFEST_PATH.read_text())
    filings = manifest.get("filings", [])
    
    print(f"Starting ingestion for {len(filings)} filings...")

    for filing in filings:
        accession = filing["accession_number"]
        
        # 1. IDEMPOTENCY CHECK: Skip if already in database
        existing = supabase_service_role.table("source_documents") \
            .select("id") \
            .eq("accession_number", accession) \
            .execute()
            
        if existing.data:
            print(f"Skipping {filing['ticker']} {filing['form']} ({accession}) - Already ingested.")
            continue

        print(f"Processing {filing['ticker']} {filing['form']} ({accession})...")
        
        # 2. Parse HTML to Markdown
        local_path = DATA_DIR / "downloads" / filing["local_path"]
        if not local_path.exists():
            print(f"  Warning: File not found at {local_path}")
            continue
            
        markdown_text = parse_sec_html_to_markdown(local_path)
        
        # 3. Save Source Document (with explicit UUID)
        doc_id = str(uuid.uuid4())  # Generate UUID explicitly
        doc_response = supabase_service_role.table("source_documents").insert({
            "id": doc_id,  # Add the ID here
            "ticker": filing["ticker"],
            "form_type": filing["form"],
            "filing_date": filing["filing_date"],
            "report_date": filing["report_date"],
            "accession_number": accession,
            "source_url": filing["source_url"],
            "local_path": str(local_path),
        }).execute()
        
        # 4. Chunk the Markdown
        chunks = chunk_markdown(markdown_text)
        print(f"  Generated {len(chunks)} chunks.")
        
        # 5. Embed and Save Chunks
        chunks_to_insert = []
        for chunk in chunks:
            try:
                embedding = get_embedding(chunk["content"])
                chunks_to_insert.append({
                    "id": str(uuid.uuid4()),  # Generate UUID explicitly
                    "source_document_id": doc_id,
                    "chunk_index": chunk["chunk_index"],
                    "section_heading": chunk["section_heading"],
                    "content": chunk["content"],
                    "embedding": embedding,
                })
            except Exception as e:
                print(f"  Error embedding chunk {chunk['chunk_index']}: {e}")

        if chunks_to_insert:
            # Insert in batches if necessary, but for 25 filings, one bulk insert is fine
            supabase_service_role.table("document_chunks").insert(chunks_to_insert).execute()
            print(f"  Saved {len(chunks_to_insert)} chunks to Supabase.")

    print("Ingestion complete!")

if __name__ == "__main__":
    run_ingestion()