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
        """Converte um documento Markdown em PDF com precisão de renderização Web."""
        import subprocess
        
        # Salva o MD num tempfile temporário na estrutura exata
        with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as tmp_md:
            tmp_md.write(markdown_text.encode("utf-8"))
            tmp_md_path = tmp_md.name
            
        pdf_path = tmp_md_path.replace(".md", ".pdf")
        
        try:
            # Inspirado no markdown2pdf-mcp, utilizamos o Node/Chromium sob o capô
            # rodando o `md-to-pdf` para processar tabelas, css e alinhamento precisamente.
            result = subprocess.run(
                ["npx", "-y", "md-to-pdf", tmp_md_path],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"Erro no motor Chromium: {result.stderr}")
            
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            return pdf_bytes
        finally:
            if os.path.exists(tmp_md_path):
                os.remove(tmp_md_path)
            if os.path.exists(pdf_path):
                os.remove(pdf_path)