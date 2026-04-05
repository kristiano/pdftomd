"""CSS templates and HTML skeletons for PDF generation."""

GITHUB_STYLE_CSS = """
@page {
    size: A4;
    margin: 2cm;
}
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Liberation Sans", Helvetica, Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    font-size: 14px;
    font-variant-ligatures: none;
}
h1, h2, h3 { border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
table { border-collapse: collapse; width: 100%; margin: 15px 0; }
th, td { border: 1px solid #dfe2e5; padding: 6px 13px; }
th { background-color: #f6f8fa; font-weight: bold; text-align: left; }
pre { background-color: #f6f8fa; padding: 16px; overflow: auto; border-radius: 3px; font-family: monospace; font-size: 13px; page-break-inside: avoid; }
code { background-color: rgba(27,31,35,0.05); padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace; font-size: 13px; }
blockquote { padding: 0 1em; color: #6a737d; border-left: 0.25em solid #dfe2e5; margin: 0; }
img { max-width: 100%; box-sizing: content-box; }

/* ========================================================
   Alertas GFM: [!NOTE], [!TIP], [!IMPORTANT], [!WARNING], [!CAUTION]
   Inspirado no estilo GitHub
   ======================================================== */
.gfm-alert {
    padding: 12px 16px;
    margin: 16px 0;
    border-radius: 6px;
    border-left: 4px solid;
    page-break-inside: avoid;
}
.gfm-alert p {
    margin: 4px 0;
}
.gfm-alert-title {
    font-weight: 700;
    font-size: 14px;
    margin-bottom: 4px !important;
}

/* NOTE - azul */
.gfm-alert-note {
    background-color: #dbeafe;
    border-left-color: #3b82f6;
    color: #1e3a5f;
}
.gfm-alert-note .gfm-alert-title { color: #1d4ed8; }

/* TIP - verde */
.gfm-alert-tip {
    background-color: #d1fae5;
    border-left-color: #10b981;
    color: #14532d;
}
.gfm-alert-tip .gfm-alert-title { color: #059669; }

/* IMPORTANT - roxo */
.gfm-alert-important {
    background-color: #ede9fe;
    border-left-color: #8b5cf6;
    color: #3b0764;
}
.gfm-alert-important .gfm-alert-title { color: #7c3aed; }

/* WARNING - amarelo */
.gfm-alert-warning {
    background-color: #fef3c7;
    border-left-color: #f59e0b;
    color: #78350f;
}
.gfm-alert-warning .gfm-alert-title { color: #d97706; }

/* CAUTION - vermelho */
.gfm-alert-caution {
    background-color: #fee2e2;
    border-left-color: #ef4444;
    color: #7f1d1d;
}
.gfm-alert-caution .gfm-alert-title { color: #dc2626; }
"""

def build_html_document(html_body: str) -> str:
    """Encapsulates raw HTML body inside a styled HTML document."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            {GITHUB_STYLE_CSS}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
