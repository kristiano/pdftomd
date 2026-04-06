import os
import fitz
import tempfile
import time
from pathlib import Path
from typing import Optional, Literal, Tuple, Callable

class PDFOptimizer:
    """
    Motor de otimização e compressão de PDF baseado no PyMuPDF.
    Oferece estratégias estruturais (preserva texto) e raster (redução agressiva).
    """

    def __init__(
        self,
        quality: int = 85,
        raster_dpi: int = 150
    ):
        self.quality = max(1, min(100, quality))
        self.raster_dpi = max(50, min(300, raster_dpi))

    def compress(
        self, 
        input_path: str, 
        method: Literal["simple", "raster"] = "simple",
        progress_callback: Optional[Callable[[float, str], bool]] = None
    ) -> Tuple[bytes, float, bool]:
        """
        Comprime um PDF e retorna os bytes resultantes, a porcentagem de redução e se foi cancelado.
        """
        input_file = Path(input_path)
        if not input_file.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")

        original_size = input_file.stat().st_size
        was_cancelled = False
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_tmp = Path(tmp_dir) / "optimized.pdf"
            
            if method == "simple":
                if progress_callback: progress_callback(0.2, "Otimizando estrutura binária...")
                self._simple_compression(input_file, output_tmp)
                if progress_callback: progress_callback(1.0, "Otimização concluída.")
            else:
                # Método Raster (Agressivo)
                was_cancelled = self._raster_compression(input_file, output_tmp, progress_callback)

            if was_cancelled:
                return b"", 0.0, True

            final_size = output_tmp.stat().st_size
            
            # Se o arquivo resultante ficou maior e é o modo simples, retorna o original
            if final_size >= original_size and method == "simple":
                with open(input_path, "rb") as f:
                    return f.read(), 0.0, False
            
            reduction = (1 - final_size / original_size) * 100
            with open(output_tmp, "rb") as f:
                return f.read(), reduction, False

    def _simple_compression(self, input_path: Path, output_path: Path):
        """Otimização estrutural avançada (Correção: Removida Linearização Depreciada)."""
        doc = fitz.open(str(input_path))
        
        # O parâmetro 'linear=True' foi depreciado nas versões recentes do PyMuPDF/MuPDF (erro code=4).
        # Removemos para garantir compatibilidade total.
        doc.save(
            str(output_path), 
            garbage=4, 
            deflate=True, 
            clean=True, 
            pretty=False
        )
        doc.close()

    def _raster_compression(self, input_path: Path, output_path: Path, progress_callback: Optional[Callable] = None) -> bool:
        """Compressão por rasterização real com controle de qualidade JPEG."""
        doc = fitz.open(str(input_path))
        new_doc = fitz.open()
        
        total_pages = len(doc)
        scale = self.raster_dpi / 72
        matrix = fitz.Matrix(scale, scale)
        
        for i, page in enumerate(doc):
            if progress_callback:
                if progress_callback((i / total_pages), f"Processando página {i+1} de {total_pages}"):
                    new_doc.close(); doc.close()
                    return True
            
            # Converter página para Pixmap
            pix = page.get_pixmap(matrix=matrix, colorspace=fitz.csRGB)
            # Codificar como JPEG
            img_data = pix.tobytes("jpeg", jpg_quality=self.quality)
            
            # Criar nova página e inserir imagem
            new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
            new_page.insert_image(page.rect, stream=img_data)
            
            # Limpeza de memória
            pix = None; img_data = None
            time.sleep(0.01) # Yielding
            
        new_doc.save(str(output_path), garbage=4, deflate=True, clean=True)
        new_doc.close(); doc.close()
        return False

def format_size(size_bytes: int) -> str:
    """Formata tamanho de arquivo em string legível."""
    size = float(size_bytes)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"
