import os
import tempfile
import markdown
from weasyprint import HTML
from core.styles import build_html_document

def generate_pdf_from_markdown(markdown_text: str) -> bytes:
    """
    Converts markdown text to a heavily-styled PDF byte array using WeasyPrint.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf_path = tmp.name
    
    try:
        html_body = markdown.markdown(
            markdown_text, 
            extensions=['tables', 'fenced_code', 'sane_lists', 'nl2br']
        )
        
        styled_html = build_html_document(html_body)
        HTML(string=styled_html).write_pdf(pdf_path)
        
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        return pdf_bytes
    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
