import streamlit as st
import os
import tempfile
import time
from leitor_pdf import Markdownify

st.set_page_config(page_title="Markdownify Universal", page_icon="📄", layout="centered")

# Injeção de CSS Profissional (Inspirado no design system gerado pelo UI-UX-Pro-Max)
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #1E293B;
}

[data-testid="stAppViewContainer"] {
    background-color: #F8FAFC;
    background-image: radial-gradient(#E2E8F0 1px, transparent 1px);
    background-size: 20px 20px;
}

h1 {
    font-weight: 700;
    color: #1E293B !important;
    letter-spacing: -0.02em;
}

h3 {
    font-weight: 600;
    color: #334155 !important;
}

/* Primary Button Styling (Orange CTA para conversão) */
div.stButton > button {
    background: linear-gradient(135deg, #F97316 0%, #EA580C 100%);
    color: white !important;
    font-weight: 600;
    border-radius: 8px;
    border: none;
    padding: 0.6rem 1.2rem;
    box-shadow: 0 4px 6px -1px rgba(249, 115, 22, 0.2), 0 2px 4px -1px rgba(249, 115, 22, 0.1);
    transition: all 0.3s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(249, 115, 22, 0.3), 0 4px 6px -2px rgba(249, 115, 22, 0.1);
    background: linear-gradient(135deg, #EA580C 0%, #C2410C 100%);
}

/* Download Button Specific (Secondary Primary) */
div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
    box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
}
div[data-testid="stDownloadButton"] > button:hover {
    background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%);
    box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
}

/* Radio buttons container (SaaS Look) */
[data-testid="stRadio"] {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    border: 1px solid #E2E8F0;
    margin-bottom: 1.5rem;
}

/* File Uploader Dropzone Styling */
[data-testid="stFileUploadDropzone"] {
    background: white;
    border: 2px dashed #94A3B8;
    border-radius: 12px;
    transition: all 0.3s ease;
}

[data-testid="stFileUploadDropzone"]:hover {
    border-color: #2563EB;
    background: #EFF6FF;
}

/* Alerts and Inputs */
.stAlert {
    border-radius: 8px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);
}

.stTextArea textarea {
    border-radius: 8px;
    border: 1px solid #CBD5E1;
}

.stTextArea textarea:focus {
    border-color: #2563EB;
    box-shadow: 0 0 0 1px #2563EB;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title("📄 Conversor Markdownify")
st.markdown("Ferramenta inspirada no robusto ecossistema `markdownify-mcp`. Transforme **qualquer arquivo** (PDF, Word, Excel, Texto) ou **URLs** (Páginas e artigos) em texto formatado `.md`.")

st.divider()

# Instancia a engine principal
markdownify = Markdownify()

# Seleção principal da ferramenta
opcao = st.radio(
    "Escolha a operação desejada:",
    ("Extrair Arquivo/PDF para Markdown", "Converter Markdown para PDF"),
    horizontal=False
)

st.divider()

if opcao == "Extrair Arquivo/PDF para Markdown":
    st.subheader("📄 Extrair Markdown de um Documento Universal")
    st.markdown("Faça o upload do seu arquivo (PDF, Word, Excel, PowerPoint) para extrair os textos e imagens formatadas.")
    
    uploaded_pdf = st.file_uploader(
        "Arraste e solte ou clique para escolher um documento", 
        type=["pdf", "docx", "doc", "xlsx", "pptx", "html"]
    )
    
    if uploaded_pdf is not None:
        st.info(f"Arquivo carregado: **{uploaded_pdf.name}**")
        
        if st.button("🚀 Converter para .md", use_container_width=True, type="primary"):
            file_size_mb = len(uploaded_pdf.getvalue()) / (1024 * 1024)
            # Estimativa básica: ~4 segundos por Megabyte do arquivo para extração pesada
            est_seconds = max(3, int(file_size_mb * 4))
            
            progress_bar = st.progress(0, text=f"0% - Iniciando conversão... (Tempo est.: ~{est_seconds}s)")
            status_text = st.empty()
            
            try:
                status_text.text("Preparando o ambiente e validando...")
                progress_bar.progress(30, text=f"30% - Alocando em memória... (Tempo est.: ~{est_seconds}s)")
                time.sleep(0.5)
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_pdf.getvalue())
                    tmp_file_path = tmp_file.name
                
                status_text.text("Lendo documento e gerando imagens embutidas...")
                progress_bar.progress(60, text=f"60% - Motor executando extração profunda... (Aguarde)")

                start_time = time.time()
                md_content = markdownify.from_file(tmp_file_path)
                elapsed = time.time() - start_time
                source_name = os.path.splitext(uploaded_pdf.name)[0]
                
                progress_bar.progress(100, text=f"100% - Pronto! Finalizado em {elapsed:.1f}s.")
                status_text.text("Conversão concluída!")
                time.sleep(0.5)
                
                progress_bar.empty()
                status_text.empty()
                
                st.success("✅ Documento Markdown gerado com sucesso!")
                
                st.download_button(
                    label="📥 Baixar Arquivo Markdown",
                    data=md_content,
                    file_name=f"{source_name}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
                
                st.divider()
                with st.expander("👀 Ver arquivo convertido (Preview)"):
                    st.markdown(md_content)
                
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ Erro durante a extração: {e}")
            finally:
                if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
                    os.remove(tmp_file_path)

elif opcao == "Converter Markdown para PDF":
    st.subheader("📝 Gerar PDF de um arquivo Markdown")
    st.markdown("Faça o upload do documento `.md` que você deseja renderizar visualmente em formato de PDF.")
    
    uploaded_md = st.file_uploader("Arraste e solte ou clique para escolher um arquivo .md", type=["md", "markdown", "txt"])
    
    if uploaded_md is not None:
        st.info(f"Arquivo carregado: **{uploaded_md.name}**")
        
        if st.button("📄 Renderizar um PDF", use_container_width=True, type="primary"):
            md_text = uploaded_md.getvalue().decode("utf-8")
            # Estimativa básica: ~1 segundo para cada 5 mil caracteres (WeasyPrint pode ser denso)
            est_seconds = max(2, int(len(md_text) / 5000))
            
            progress_bar = st.progress(0, text=f"0% - Preparando renderização... (Tempo est.: ~{est_seconds}s)")
            status_text = st.empty()
            
            try:
                status_text.text("Lendo o documento texto...")
                progress_bar.progress(30, text=f"30% - Interpretando Markdown... (Tempo est.: ~{est_seconds}s)")
                time.sleep(0.5)
                
                status_text.text("Estruturando as páginas, tabelas e parágrafos do PDF...")
                progress_bar.progress(60, text=f"60% - Motor WeasyPrint renderizando pixels... (Aguarde)")
                
                start_time = time.time()
                pdf_bytes = markdownify.to_pdf(md_text)
                elapsed = time.time() - start_time
                
                source_name = os.path.splitext(uploaded_md.name)[0]
                
                progress_bar.progress(100, text=f"100% - Documento gerado em {elapsed:.1f}s.")
                status_text.text("Renderização concluída!")
                time.sleep(0.5)
                
                progress_bar.empty()
                status_text.empty()
                
                st.success("✅ PDF estruturado com sucesso!")
                
                st.download_button(
                    label="📥 Baixar novo arquivo gerado (.pdf)",
                    data=pdf_bytes,
                    file_name=f"{source_name}_gerado.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ Erro crítico ao converter para PDF: {e}")
