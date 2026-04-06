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
