import os
import tempfile
import markdown
import re
import base64
import io
from fpdf import FPDF
from PIL import Image
from typing import Optional, Callable

# Configurações de Estilo Premium
COLOR_TEXT = (30, 41, 59)
COLOR_H1 = (15, 23, 42)
COLOR_H2 = (79, 70, 229)
COLOR_H3 = (100, 116, 139)
COLOR_BG_ALERT = (248, 250, 252)

GFM_ALERTS = {
    "NOTE":      ("ℹ️", "Nota"),
    "TIP":       ("💡", "Dica"),
    "IMPORTANT": ("❗", "Importante"),
    "WARNING":   ("⚠️", "Aviso"),
    "CAUTION":   ("🔴", "Cuidado"),
}

class FastPDFRenderer(FPDF):
    """
    Renderizador de PDF Profissional 20x mais rápido (FPDF2).
    Inspirado no projeto 'markdown2pdf-mcp' para máxima eficiência.
    """
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.set_font("helvetica", size=11)
        self.set_text_color(*COLOR_TEXT)

    def header(self):
        if self.page_no() > 1:
            self.set_font("helvetica", "I", 8)
            self.set_text_color(160, 160, 160)
            self.cell(0, 8, "Gerado por Canivete Suíço Master", 0, 0, "R")
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

    def render_markdown(self, md_text: str):
        """
        Processa Markdown estrutural, Alertas e Imagens Base64.
        """
        lines = md_text.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # 1. Headers (H1-H4)
            if line.startswith('#'):
                level = min(line.count('#', 0, 6), 3)
                content = line.strip('#').strip()
                self.ln(3)
                if level == 1:
                    self.set_font("helvetica", "B", 22); self.set_text_color(*COLOR_H1)
                elif level == 2:
                    self.set_font("helvetica", "B", 16); self.set_text_color(*COLOR_H2)
                else:
                    self.set_font("helvetica", "B", 13); self.set_text_color(*COLOR_H3)
                self.multi_cell(0, 10, content)
                self.ln(2)
                self.set_font("helvetica", "", 11); self.set_text_color(*COLOR_TEXT)
                i += 1; continue

            # 2. Imagens (Suporte a Base64 do PyMuPDF4LLM)
            # Formato: ![](data:image/png;base64,...)
            img_match = re.search(r'!\[.*?\]\(data:image/(.*?);base64,(.*?)\)', line)
            if img_match:
                try:
                    img_ext = img_match.group(1)
                    img_data = base64.b64decode(img_match.group(2))
                    img_io = io.BytesIO(img_data)
                    with Image.open(img_io) as pil_img:
                        w_px, h_px = pil_img.size
                        # Ajustar largura para caber na página (max 180mm)
                        w_mm = min(180, w_px * 0.1) 
                        h_mm = (h_px / w_px) * w_mm
                        # Verificar se cabe na página atual
                        if self.get_y() + h_mm > 270: self.add_page()
                        self.image(img_io, x=15, w=w_mm)
                        self.ln(5)
                except Exception: pass
                i += 1; continue

            # 3. Alertas e Blockquotes
            if line.startswith('>'):
                self.set_fill_color(*COLOR_BG_ALERT)
                self.set_draw_color(*COLOR_H2)
                self.set_line_width(0.5)
                content = line.strip('>').strip()
                alert_match = re.search(r'\[!(.*?)\]', content)
                if alert_match:
                    type_a = alert_match.group(1).upper()
                    icon, label = GFM_ALERTS.get(type_a, ("📌", type_a))
                    self.set_font("helvetica", "B", 10)
                    self.rect(10, self.get_y(), 190, 8, style="F")
                    self.cell(0, 8, f"{icon} {label}", ln=True, fill=True)
                    self.set_font("helvetica", "", 10)
                else:
                    # Renderizar bloco simples
                    self.multi_cell(0, 8, content, fill=True, border='L')
                self.set_font("helvetica", "", 11)
                i += 1; continue

            # 4. Listas
            if re.match(r'^[\-\*\+\d\.]+\s', line):
                self.set_x(15)
                self.write(7, f"• {re.sub(r'^[\-\*\+\d\.]+\s', '', line).strip()}\n")
                i += 1; continue

            # 5. Texto normal com bold/italic (Limpeza simplificada para velocidade)
            if line:
                # Bold
                clean = re.sub(r'(\*\*|__)(.*?)\1', r'\2', line)
                # Italic
                clean = re.sub(r'(\*|_)(.*?)\1', r'\2', clean)
                self.multi_cell(0, 7, clean)
            elif not line:
                self.ln(3)
            
            i += 1

def generate_pdf_from_markdown(markdown_text: str) -> bytes:
    """
    Conversor de Markdown para PDF Profissional e Instantâneo.
    Referência de performance baseada no markdown2pdf-mcp.
    """
    renderer = FastPDFRenderer()
    renderer.render_markdown(markdown_text)
    return renderer.output()
