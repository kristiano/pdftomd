import os
import tempfile
import markdown
import re
import base64
import io
from fpdf import FPDF
from PIL import Image
from typing import Optional, Callable

# Token de cores Slate/Indigo
COLOR_TEXT = (30, 41, 59)
COLOR_H1 = (15, 23, 42)
COLOR_H2 = (79, 70, 229)
COLOR_H3 = (100, 116, 139)

GFM_ALERTS = {
    "NOTE": ("ℹ️", "Nota"),
    "TIP": ("💡", "Dica"),
    "IMPORTANT": ("❗", "Importante"),
    "WARNING": ("⚠️", "Aviso"),
    "CAUTION": ("🔴", "Cuidado"),
}

class FastPDFRenderer(FPDF):
    """
    Renderizador Robusto e Veloz.
    Protegido contra estouro de largura horizontal.
    """
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_left_margin(15)
        self.set_right_margin(15)
        self.add_page()
        self.set_font("helvetica", size=11)
        self.set_text_color(*COLOR_TEXT)

    def render_markdown(self, md_text: str):
        lines = md_text.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            # Resetar X para a margem esquerda para cada linha para evitar 'Not enough horizontal space'
            self.set_x(self.l_margin)
            
            if not line:
                self.ln(4); i += 1; continue

            # 🛑 SEGURANÇA: Ignorar linhas gigantes sem espaços (Provável lixo binário ou Base64 mal formatado)
            if len(line) > 1000 and " " not in line[:500]:
                i += 1; continue

            # 1. Headers
            if line.startswith('#'):
                level = min(line.count('#', 0, 6), 3)
                content = line.strip('#').strip()
                self.ln(3)
                if level == 1:
                    self.set_font("helvetica", "B", 20); self.set_text_color(*COLOR_H1)
                elif level == 2:
                    self.set_font("helvetica", "B", 15); self.set_text_color(*COLOR_H2)
                else:
                    self.set_font("helvetica", "B", 12); self.set_text_color(*COLOR_H3)
                self.multi_cell(0, 10, content)
                self.ln(1)
                self.set_font("helvetica", "", 11); self.set_text_color(*COLOR_TEXT)
                i += 1; continue

            # 2. Imagens Base64 (Otimizado)
            img_match = re.search(r'!\[.*?\]\(data:image/(.*?);base64,(.*?)\)', line)
            if img_match:
                try:
                    img_data = base64.b64decode(img_match.group(2))
                    img_io = io.BytesIO(img_data)
                    with Image.open(img_io) as pil_img:
                        w_px, h_px = pil_img.size
                        w_mm = min(170, w_px * 0.12) # Ajuste de DPI
                        h_mm = (h_px / w_px) * w_mm
                        if self.get_y() + h_mm > 270: self.add_page()
                        self.image(img_io, x=self.l_margin, w=w_mm)
                        self.ln(h_mm + 5)
                except Exception: pass
                i += 1; continue

            # 3. Alertas e Blockquotes
            if line.startswith('>'):
                content = line.strip('>').strip()
                self.set_fill_color(248, 250, 252)
                self.set_draw_color(*COLOR_H2)
                self.multi_cell(0, 8, content, fill=True, border='L')
                i += 1; continue

            # 4. Listas
            if re.match(r'^[\-\*\+\d\.]+\s', line):
                content = re.sub(r'^[\-\*\+\d\.]+\s', '', line).strip()
                self.set_x(self.l_margin + 5) # Indentação segura
                self.multi_cell(0, 7, f"• {content}")
                i += 1; continue

            # 5. Texto Normal
            # Bold/Italic cleaning for speed and compatibility
            clean = re.sub(r'(\*\*|__|\*|_)(.*?)\1', r'\2', line)
            # Substituir caracteres não suportados pelo encoding latin-1 (padrão FPDF2)
            clean = clean.encode('latin-1', 'replace').decode('latin-1')
            
            try:
                self.multi_cell(0, 7, clean)
            except Exception:
                # Fallback se encontrar caracteres que quebram o cálculo de largura
                pass
            
            i += 1

def generate_pdf_from_markdown(markdown_text: str) -> bytes:
    """
    Geração Robusta (Fix: Not enough horizontal space).
    """
    renderer = FastPDFRenderer()
    renderer.render_markdown(markdown_text)
    return renderer.output()
