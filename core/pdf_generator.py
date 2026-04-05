import os
import re
import tempfile
import markdown
from weasyprint import HTML
from core.styles import build_html_document

# Mapeamento dos alertas GFM para ícones e classes CSS
GFM_ALERTS = {
    "NOTE":      ("ℹ️", "Nota"),
    "TIP":       ("💡", "Dica"),
    "IMPORTANT": ("❗", "Importante"),
    "WARNING":   ("⚠️", "Aviso"),
    "CAUTION":   ("🔴", "Cuidado"),
}


def _preprocess_gfm_alerts(md_text: str) -> str:
    """
    Converte blocos de alerta GFM (> [!TYPE]) em HTML estilizado
    antes de passar pelo parser markdown padrão.
    
    Entrada esperada:
        > [!IMPORTANT]
        > Texto da mensagem
        > pode ter múltiplas linhas
    
    Saída: bloco <div class="gfm-alert gfm-alert-important">...</div>
    """
    # Regex que captura o bloco inteiro do alerta:
    # - Linha inicial: > [!TIPO]  (com possíveis espaços)
    # - Linhas seguintes que começam com >
    pattern = re.compile(
        r'^(?:>\s*)\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*\n'
        r'((?:>.*\n?)*)',
        re.MULTILINE | re.IGNORECASE
    )

    def replace_alert(match):
        alert_type = match.group(1).upper()
        raw_body = match.group(2)

        # Remove o prefixo '>' de cada linha do corpo
        lines = []
        for line in raw_body.split('\n'):
            cleaned = re.sub(r'^>\s?', '', line)
            lines.append(cleaned)
        body_text = '\n'.join(lines).strip()

        # Converte o corpo do alerta de markdown para HTML (suporta negrito, links, etc.)
        body_html = markdown.markdown(body_text, extensions=['tables', 'fenced_code'])

        icon, label = GFM_ALERTS.get(alert_type, ("📌", alert_type))
        css_class = alert_type.lower()

        return (
            f'<div class="gfm-alert gfm-alert-{css_class}">'
            f'<p class="gfm-alert-title">{icon} {label}</p>'
            f'{body_html}'
            f'</div>\n\n'
        )

    return pattern.sub(replace_alert, md_text)


def generate_pdf_from_markdown(markdown_text: str) -> bytes:
    """
    Converts markdown text to a heavily-styled PDF byte array using WeasyPrint.
    Inclui pré-processamento para alertas GFM ([!NOTE], [!TIP], [!IMPORTANT], etc.)
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf_path = tmp.name

    try:
        # 1. Pré-processa alertas GFM antes do parser markdown
        preprocessed_text = _preprocess_gfm_alerts(markdown_text)

        # 2. Converte markdown restante para HTML
        html_body = markdown.markdown(
            preprocessed_text,
            extensions=['tables', 'fenced_code', 'sane_lists', 'nl2br']
        )

        # 3. Monta documento HTML completo com estilos e gera PDF
        styled_html = build_html_document(html_body)
        HTML(string=styled_html).write_pdf(pdf_path)

        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        return pdf_bytes
    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
