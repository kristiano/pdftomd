from core import (
    extract_markdown_from_file,
    fetch_and_extract_from_url,
    generate_pdf_from_markdown
)

class Markdownify:
    """
    Facade Controller (Orquestrador) padronizado.
    Delega a lógica de conversão trazendo suporte universal a URLs e Múltiplos Arquivos
    através da integração com os serviços em /core/.
    """
    def __init__(self):
        pass

    def from_file(self, file_path: str) -> str:
        """Delega a extração de arquivos para o serviço de domínio extrator."""
        return extract_markdown_from_file(file_path)

    def from_url(self, url: str) -> str:
        """Delega as complexidades de rede para o Handler HTTP."""
        return fetch_and_extract_from_url(url)
                
    def to_pdf(self, markdown_text: str) -> bytes:
        """Transfere o processamento de renderização WeasyPrint para o motor de PDF isolado."""
        return generate_pdf_from_markdown(markdown_text)