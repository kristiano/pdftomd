import os
import tempfile
import requests
from core.extractor import extract_markdown_from_file

def fetch_and_extract_from_url(url: str) -> str:
    """
    Downloads a file or webpage directly from an HTTP URL into a temp file, 
    and cascades it into the internal extractor.
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()
    
    ext = url.split('.')[-1].split('?')[0]
    if len(ext) > 5 or "/" in ext: 
        ext = "html"
        
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name
        
    try:
        return extract_markdown_from_file(tmp_path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
