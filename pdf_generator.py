import os
import tempfile
import markdown
import re
import base64
import io
from fpdf import FPDF
from PIL import Image
from typing import Optional, Callable

# Design Tokens (Slate/Indigo)
COLOR_TEXT = (30, 41, 59)
COLOR_H1 = (15, 23, 42)
COLOR_H2 = (79, 70, 229)
COLOR_H3 = (100, 116, 139)

class SafePDFRenderer(FPDF):
    """
    Renderizador Iron-Clad (À prova de falhas de largura).
    Projetado para lidar com documentos Markdown 'sujos' sem crashar.
    """
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        # Margens fixas robustas (A4: 210mm total)
        self.l_margin_fix = 20
        self.r_margin_fix = 20
        self.effective_width = 170 # 210 - 20 - 20
        
        self.set_left_margin(self.l_margin_fix)
        self.set_right_margin(self.r_margin_fix)
        self.add_page()
        self.set_font("helvetica", size=11)
        self.set_text_color(*COLOR_TEXT)

    def render_markdown(self, md_text: str):
        # Limpar o MD de possíveis caracteres nulos ou de controle que quebram o FPDF2
        md_text = md_text.replace('\x00', '').replace('\r', '')
        lines = md_text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # 1. Garantir reset de posição a cada linha para evitar drift horizontal
            self.set_x(self.l_margin_fix)
            
            if not line:
                self.ln(5); continue

            # 2. Ignorar Base64 ou ruído binário que não foi capturado pelas regex
            if len(line) > 500 and " " not in line[:200]:
                continue

            # 3. Headers
            if line.startswith('#'):
                level = min(line.count('#', 0, 6), 3)
                content = line.strip('#').strip()
                self.ln(2)
                if level == 1:
                    self.set_font("helvetica", "B", 18); self.set_text_color(*COLOR_H1)
                elif level == 2:
                    self.set_font("helvetica", "B", 14); self.set_text_color(*COLOR_H2)
                else:
                    self.set_font("helvetica", "B", 11); self.set_text_color(*COLOR_H3)
                
                self.multi_cell(self.effective_width, 10, content)
                self.set_font("helvetica", "", 11); self.set_text_color(*COLOR_TEXT)
                self.ln(2)
                continue

            # 4. Imagens Base64
            img_match = re.search(r'!\[.*?\]\(data:image/(.*?);base64,(.*?)\)', line)
            if img_match:
                try:
                    img_data = base64.b64decode(img_match.group(2))
                    img_io = io.BytesIO(img_data)
                    with Image.open(img_io) as pil_img:
                        w_px, h_px = pil_img.size
                        # Max 150mm para segurança total
                        w_mm = min(150, w_px * 0.1) 
                        h_mm = (h_px / w_px) * w_mm
                        if self.get_y() + h_mm > 270: self.add_page()
                        self.image(img_io, x=self.l_margin_fix, w=w_mm)
                        self.ln(h_mm + 5)
                except Exception: pass
                continue

            # 5. Blocos de Citação
            if line.startswith('>'):
                content = line.strip('>').strip()
                self.set_draw_color(*COLOR_H2)
                self.set_fill_color(248, 250, 252)
                # Usar largura fixa em vez de 0 para garantir que não estoura
                self.multi_cell(self.effective_width, 8, content, fill=True, border='L')
                self.ln(1)
                continue

            # 6. Texto Normal (Sanitização Agressiva)
            # Remove MD residual e limpa caracteres não-latin1
            clean = re.sub(r'(\*\*|__|\*|_)(.*?)\1', r'\2', line)
            clean = clean.encode('ascii', 'replace').decode('ascii')
            
            try:
                # Sempre usar a largura efetiva calculada (170mm) para evitar erros do FPDF2
                self.multi_cell(self.effective_width, 7, clean)
            except Exception:
                # Se falhar mesmo assim, ignora a linha problemática
                pass

def generate_pdf_from_markdown(markdown_text: str) -> bytes:
    """
    Geração à prova de erros de layout (v2.8.1).
    """
    renderer = SafePDFRenderer()
    renderer.render_markdown(markdown_text)
    return renderer.output()
