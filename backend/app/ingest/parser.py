# backend/app/ingest/parser.py
from pathlib import Path
from bs4 import BeautifulSoup
from markdownify import markdownify as md

def parse_sec_html_to_markdown(file_path: Path) -> str:
    """
    Reads an SEC 10-K HTML file and converts it to clean Markdown.
    """
    html_content = file_path.read_text(encoding="utf-8")
    
    # Parse HTML and remove noise
    soup = BeautifulSoup(html_content, "html.parser")
    for script in soup(["script", "style"]):
        script.decompose()
        
    # Convert to Markdown
    markdown_text = md(str(soup), heading_style="ATX")
    
    # Clean up excessive newlines
    import re
    markdown_text = re.sub(r'\n{3,}', '\n\n', markdown_text)
    
    return markdown_text.strip()