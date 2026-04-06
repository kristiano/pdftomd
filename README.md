# 📄 Document Master Ultra (v2.5)

Uma suíte poderosa e profissional para processamento de documentos, construída com [Streamlit](https://streamlit.io/) e os motores de processamento mais avançados do mercado (`PyMuPDF`, `WeasyPrint` e `MarkItDown`).

Desenvolvido por **Kristiano Plácido**.

---

## ✨ Funcionalidades Principais

### 1. 📂 Extração para Markdown (.md)
*   **Alta Fidelidade**: Conversão de PDFs complexos em Markdown estruturado.
*   **Layout Preservation**: Suporte a detecção de colunas, tabelas e listas complexas através do motor `pymupdf.layout`.
*   **Modo Imagem**: Opção para embutir imagens do PDF diretamente no Markdown em formato base64.
*   **Universal**: Suporta também arquivos Word (`.docx`), Excel (`.xlsx`), PowerPoint (`.pptx`) e HTML.

### 2. 📝 Renderização de PDF Profissional
*   **Markdown → PDF**: Transforme seus arquivos Markdown em documentos PDF com estilo limpo e profissional (GitHub Style).
*   **Precisão**: Renderização via `WeasyPrint` garantindo que listas, kdb-tags e tabelas mantenham a formatação perfeita.

### 3. ⚡ Otimização & Compressão Inteligente
*   **Modo Simples**: Redução de tamanho através de limpeza estrutural e compressão de fluxos de objetos, preservando o texto pesquisável.
*   **Modo Agressivo (Raster)**: Conversão de páginas em imagens otimizadas para reduções drásticas de tamanho em arquivos escaneados ou muito pesados.
*   **Dashboard de Métricas**: Visualização em tempo real da economia de espaço e comparação entre o arquivo original e o otimizado.

---

## 🛠️ Tecnologias Utilizadas

*   **Streamlit**: Interface web moderna e responsiva.
*   **PyMuPDF (fitz)**: Manipulação e otimização profunda de PDFs.
*   **PyMuPDF4LLM**: Extração de Markdown otimizada para Modelos de Linguagem.
*   **WeasyPrint**: Motor de renderização CSS/HTML para criação de PDFs.
*   **MarkItDown**: Conversão universal de arquivos Office para Markdown.

---

## ⚙️ Instalação e Uso Local

### Pré-requisitos
*   **Python 3.10+** instalado.

### Passo a Passo

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/leitor-pdf-md.git
   cd leitor-pdf-md
   ```

2. **Crie e ative um ambiente virtual**:
   ```bash
   # MacOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate

   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Inicie a aplicação**:
   ```bash
   streamlit run app.py
   ```

---

## 🚀 Como usar

1.  Acesse o menu lateral (**Menu de Ferramentas**) para escolher a operação desejada.
2.  Faça o upload do seu arquivo no campo central.
3.  Ajuste as configurações (como qualidade visual ou modo de extração).
4.  Clique no botão de ação principal (botão colorido).
5.  Visualize o resultado no **Preview** ou clique no botão verde para **Baixar** o arquivo processado.

---

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se à vontade para contribuir!

---
*Powered by Kristiano Plácido.*
