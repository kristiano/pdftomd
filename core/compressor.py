import os
import fitz
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Literal, Tuple

class PDFOptimizer:
    """
    Motor de otimização e compressão de PDF baseado no PyMuPDF.
    Oferece estratégias estruturais (preserva texto) e raster (redução agressiva).
    """

    def __init__(
        self,
        quality: int = 85,
        raster_dpi: int = 150,
        keep_text: bool = True
    ):
        self.quality = max(1, min(100, quality))
        self.raster_dpi = max(50, min(300, raster_dpi))
        self.keep_text = keep_text

    def compress(
        self, 
        input_path: str, 
        method: Literal["simple", "raster"] = "simple"
    ) -> Tuple[bytes, float]:
        """
        Comprime um PDF e retorna os bytes resultantes e a porcentagem de redução.
        """
        input_file = Path(input_path)
        if not input_file.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")

        original_size = input_file.stat().st_size
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_tmp = Path(tmp_dir) / "optimized.pdf"
            
            if method == "simple" or self.keep_text:
                self._simple_compression(input_file, output_tmp)
            else:
                self._raster_compression(input_file, output_tmp)

            # Garantir que não ficou maior que o original
            final_size = output_tmp.stat().st_size
            if final_size > original_size:
                # Se ficou maior, retornamos o original original
                with open(input_path, "rb") as f:
                    return f.read(), 0.0
            
            reduction = (1 - final_size / original_size) * 100
            with open(output_tmp, "rb") as f:
                return f.read(), reduction

    def _simple_compression(self, input_path: Path, output_path: Path):
        """Otimização estrutural (remove objetos duplicados, limpa metadados inúteis)."""
        doc = fitz.open(str(input_path))
        doc.save(
            str(output_path),
            garbage=4,
            deflate=True,
            clean=True
        )
        doc.close()

    def _raster_compression(self, input_path: Path, output_path: Path):
        """Compressão por rasterização (converte páginas em imagens). Perde seleção de texto."""
        doc = fitz.open(str(input_path))
        new_doc = fitz.open()
        
        scale = self.raster_dpi / 72
        matrix = fitz.Matrix(scale, scale)
        
        for page in doc:
            pix = page.get_pixmap(matrix=matrix, colorspace=fitz.csRGB)
            img_data = pix.tobytes("jpeg", jpg_quality=self.quality)
            
            # Criar página com dimensões originais
            new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
            new_page.insert_image(page.rect, stream=img_data)
            
        new_doc.save(
            str(output_path),
            garbage=4,
            deflate=True,
            clean=True
        )
        new_doc.close()
        doc.close()

def format_size(size_bytes: int) -> str:
    """Formata tamanho de arquivo em string legível."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"
