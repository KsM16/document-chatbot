# backend/app/ingest/demo_runner.py
import json
import uuid
import time
from pathlib import Path
from app.database.supabase import supabase_service_role
from .parser import parse_sec_html_to_markdown
from .chunker import chunk_markdown
from .embedder import get_embedding

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"
MANIFEST_PATH = DATA_DIR / "downloads" / "manifest.json"

def run_demo_ingestion():
    if not MANIFEST_PATH.exists():
        print("Error: manifest.json not found.")
        return

    manifest = json.loads(MANIFEST_PATH.read_text())
    filings = manifest.get("filings", [])
    
    # SAFETY: Only pick the first 2 filings for the demo (e.g., 1 AAPL, 1 MSFT)
    demo_filings = []
    for f in filings:
        if f['ticker'] == 'AAPL' and not any(x['ticker'] == 'AAPL' for x in demo_filings):
            demo_filings.append(f)
        elif f['ticker'] == 'MSFT' and not any(x['ticker'] == 'MSFT' for x in demo_filings):
            demo_filings.append(f)
            
        if len(demo_filings) == 2:
            break

    print(f"Starting DEMO ingestion for {len(demo_filings)} filings...")

    for filing in demo_filings:
        accession = filing["accession_number"]
        
        # 1. IDEMPOTENCY CHECK (Same as main runner)
        existing = supabase_service_role.table("source_documents") \
            .select("id") \
            .eq("accession_number", accession) \
            .execute()
            
        if existing.data:
            print(f"Skipping {filing['ticker']} - Already ingested.")
            continue

        print(f"Processing {filing['ticker']} {filing['form']}...")
        
        local_path = DATA_DIR / "downloads" / filing["local_path"]
        if not local_path.exists():
            print(f"  Warning: File not found at {local_path}")
            continue
            
        markdown_text = parse_sec_html_to_markdown(local_path)
        
        doc_id = str(uuid.uuid4())
        supabase_service_role.table("source_documents").insert({
            "id": doc_id,
            "ticker": filing["ticker"],
            "form_type": filing["form"],
            "filing_date": filing["filing_date"],
            "report_date": filing["report_date"],
            "accession_number": accession,
            "source_url": filing["source_url"],
            "local_path": str(local_path),
        }).execute()
        
        chunks = chunk_markdown(markdown_text)
        print(f"  Generated {len(chunks)} chunks. Embedding (this will take ~5 mins)...")
        
        chunks_to_insert = []
        for chunk in chunks:
            try:
                # The 0.5s delay and 1536-dim fix are inside your updated embedder.py
                embedding = get_embedding(chunk["content"])
                chunks_to_insert.append({
                    "id": str(uuid.uuid4()),
                    "source_document_id": doc_id,
                    "chunk_index": chunk["chunk_index"],
                    "section_heading": chunk["section_heading"],
                    "content": chunk["content"],
                    "embedding": embedding,
                })
            except Exception as e:
                print(f"  Error embedding chunk {chunk['chunk_index']}: {e}")

        if chunks_to_insert:
            supabase_service_role.table("document_chunks").insert(chunks_to_insert).execute()
            print(f"  Successfully saved {len(chunks_to_insert)} chunks for {filing['ticker']}!")

    print("\nDEMO INGESTION COMPLETE! You have enough data for a working prototype.")

if __name__ == "__main__":
    run_demo_ingestion()