import os
import fitz
import pymupdf4llm
from markitdown import MarkItDown

# Ativa recursos de layout avançado do PyMuPDF se disponíveis
try:
    import pymupdf.layout
except ImportError:
    pass

def extract_markdown_from_file(file_path: str, embed_images: bool = True) -> str:
    """
    Realiza a extração de Markdown de diversos tipos de arquivos.
    Para PDFs, utiliza o motor PyMuPDF4LLM com foco em preservação de estrutura.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
    ext = file_path.lower().split('.')[-1]
        
    if ext == "doc":
        raise ValueError("O formato antigo do Word (.doc) não é suportado pelo motor universal. "
                         "Por favor, salve o arquivo como .docx no Word e tente novamente.")
        
    if ext == "pdf":
        # Se embed_images for True, o usuário deseja fidelidade visual (estilo)
        # Usamos page_chunks para iterar e garantir que separadores de página sejam incluídos
        if embed_images:
            chunks = pymupdf4llm.to_markdown(
                file_path, 
                embed_images=True, 
                page_chunks=True
            )
            # Unindo com separadores horizontais Markdown (---) para manter o "estilo" de páginas
            md_pages = [chunk["text"] for chunk in chunks]
            return "\n\n---\n\n".join(md_pages)
        else:
            # Modo LLM: Texto contínuo e limpo, sem imagens
            return pymupdf4llm.to_markdown(file_path, embed_images=False)
        
    try:
        md_engine = MarkItDown()
        result = md_engine.convert(file_path)
        return result.text_content
    except Exception as e:
        raise RuntimeError(f"O arquivo .{ext} não foi convertido corretamente. Erro: {str(e)}")
