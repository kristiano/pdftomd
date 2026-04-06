import os
import pymupdf4llm
from markitdown import MarkItDown

def extract_markdown_from_file(file_path: str, embed_images: bool = True) -> str:
    """
    Handles internal business logic to extract Markdown from multiple file types.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
    ext = file_path.lower().split('.')[-1]
        
    if ext == "doc":
        raise ValueError("O formato antigo do Word (.doc) não é suportado pelo motor universal. Por favor, salve o arquivo como .docx no Word e tente novamente.")
        
    if ext == "pdf":
        return pymupdf4llm.to_markdown(file_path, embed_images=embed_images)
        
    try:
        md_engine = MarkItDown()
        result = md_engine.convert(file_path)
        return result.text_content
    except Exception as e:
        raise RuntimeError(f"O arquivo {ext} não foi convertido corretamente. O motor informou: {str(e)}")
