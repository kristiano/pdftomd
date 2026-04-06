import os
import re
import fitz
import pymupdf4llm
from markitdown import MarkItDown
from typing import Optional, Callable

def extract_markdown_from_file(file_path: str, embed_images: bool = True, progress_callback: Optional[Callable[[float, str], bool]] = None) -> str:
    """
    Realiza a extração de Markdown. Se embed_images for False, limpa marcadores de imagem omitida.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
    ext = file_path.lower().split('.')[-1]
        
    if ext == "pdf":
        doc = fitz.open(file_path)
        total_pages = len(doc)
        md_pages = []
        
        # Expressão regular para remover o marcador de imagens omitidas do PyMuPDF4LLM
        omitted_img_pattern = r"\*\*==> picture \[.*?\] intentionally omitted <==\*\*"
        
        for i in range(total_pages):
            if progress_callback:
                if progress_callback((i / total_pages), f"Extraindo página {i+1} de {total_pages}..."):
                    break
            
            # Extrair Markdown da página individual
            page_md = pymupdf4llm.to_markdown(doc, pages=[i], embed_images=embed_images)
            
            # Se o usuário NÃO quer imagens, limpar os placeholders barulhentos
            if not embed_images:
                page_md = re.sub(omitted_img_pattern, "", page_md)
            
            md_pages.append(page_md)
            
        doc.close()
        separator = "\n\n---\n\n" if embed_images else "\n\n"
        return separator.join(md_pages)
        
    # Outros formatos (Word/Excel) via MarkItDown
    if progress_callback: progress_callback(0.3, f"Analisando .{ext}...")
    try:
        md_engine = MarkItDown()
        result = md_engine.convert(file_path)
        if progress_callback: progress_callback(1.0, "Pronto!")
        return result.text_content
    except Exception as e:
        raise RuntimeError(f"Erro na conversão .{ext}: {str(e)}")
