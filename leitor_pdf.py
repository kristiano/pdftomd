import os
import tempfile
import requests
import pymupdf4llm
from markitdown import MarkItDown

class Markdownify:
    """
    Classe baseada nos princípios do mcp-markdownify-server.
    Isola a lógica de conversão trazendo suporte universal a URLs e Múltiplos Arquivos.
    """
    def __init__(self):
        self.md = MarkItDown()

    def from_file(self, file_path: str) -> str:
        """Converte um arquivo local para Markdown."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
            
        ext = file_path.lower().split('.')[-1]
            
        # Tratamento especial para formatos que causam confusão
        if ext == "doc":
            raise ValueError("O formato antigo do Word (.doc) não é suportado pelo motor universal. Por favor, salve o arquivo como .docx no Word e tente novamente.")
            
        # Para PDFs, usamos o motor especializado anterior para manter a qualidade original
        if ext == "pdf":
            # Agora extrai também as imagens e anexa via base64 inline no markdown!
            return pymupdf4llm.to_markdown(file_path, embed_images=True)
            
        # Para os demais formatos (docx, xlsx, pptx, html etc), usamos o markitdown
        try:
            result = self.md.convert(file_path)
            return result.text_content
        except Exception as e:
            # Captura de erro enriquecida se o formato (ex: .docx) falhar
            raise RuntimeError(f"O arquivo {ext} não foi convertido corretamente. O motor informou: {str(e)}")

    def from_url(self, url: str) -> str:
        """Realiza o fetch de uma URL (página web ou arquivo remoto) e converte para Markdown."""
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        
        # Descrubrindo se tem extensão na URL
        ext = url.split('.')[-1].split('?')[0]
        if len(ext) > 5 or "/" in ext: 
            ext = "html" # Default to html if no clear extension
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name
            
        try:
            return self.from_file(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                
    def to_pdf(self, markdown_text: str) -> bytes:
        """Converte um documento Markdown em PDF utilizando motor WeasyPrint moderno p/ precisão máxima na Nuvem."""
        import markdown
        from weasyprint import HTML
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf_path = tmp.name
        
        try:
            # Processa o markdown com as extensões avançadas
            html_body = markdown.markdown(
                markdown_text, 
                extensions=['tables', 'fenced_code', 'sane_lists', 'nl2br']
            )
            
            # Encapsulando em HTML com um CSS elegante imitando o GitHub para garantir 100% de alinhamento
            styled_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    @page {{
                        size: A4;
                        margin: 2cm;
                    }}
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji";
                        line-height: 1.6;
                        color: #333;
                        font-size: 14px;
                    }}
                    h1, h2, h3 {{ border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }}
                    table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
                    th, td {{ border: 1px solid #dfe2e5; padding: 6px 13px; }}
                    th {{ background-color: #f6f8fa; font-weight: bold; text-align: left; }}
                    pre {{ background-color: #f6f8fa; padding: 16px; overflow: auto; border-radius: 3px; font-family: monospace; font-size: 13px; page-break-inside: avoid; }}
                    code {{ background-color: rgba(27,31,35,0.05); padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace; font-size: 13px; }}
                    blockquote {{ padding: 0 1em; color: #6a737d; border-left: 0.25em solid #dfe2e5; margin: 0; }}
                    img {{ max-width: 100%; box-sizing: content-box; }}
                </style>
            </head>
            <body>
                {html_body}
            </body>
            </html>
            """
            
            # Gera o PDF via WeasyPrint direto do HTML
            HTML(string=styled_html).write_pdf(pdf_path)
            
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            return pdf_bytes
        finally:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)