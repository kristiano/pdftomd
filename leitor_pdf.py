from core import (
    extract_markdown_from_file,
    fetch_and_extract_from_url,
    generate_pdf_from_markdown,
    PDFOptimizer
)
from typing import Optional, Callable

class Markdownify:
    """
    Facade Controller (Orquestrador) padronizado.
    Agora com suporte unificado a progress_callback para telemetria em todas as ferramentas.
    """
    def __init__(self):
        pass

    def from_file(self, file_path: str, embed_images: bool = True, progress_callback: Optional[Callable] = None) -> str:
        """Delega a extração para o serviço de domínio com suporte a barra de progresso."""
        return extract_markdown_from_file(file_path, embed_images=embed_images, progress_callback=progress_callback)

    def from_url(self, url: str) -> str:
        """Delega à rede."""
        return fetch_and_extract_from_url(url)
                
    def to_pdf(self, markdown_text: str, progress_callback: Optional[Callable] = None) -> bytes:
        """Renderiza Markdown para PDF com feedback de progresso."""
        if progress_callback: progress_callback(0.5, "Desenhando layout e carregando fontes...")
        return generate_pdf_from_markdown(markdown_text)

    def optimize_pdf(self, file_path: str, method: str = "simple", quality: int = 85, dpi: int = 150, progress_callback: Optional[Callable] = None) -> tuple:
        """Otimiza um arquivo PDF reduzindo seu tamanho."""
        optimizer = PDFOptimizer(quality=quality, raster_dpi=dpi)
        return optimizer.compress(file_path, method=method, progress_callback=progress_callback)