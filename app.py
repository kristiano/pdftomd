import streamlit as st
import os
import tempfile
import time
from leitor_pdf import Markdownify
from core import format_size

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

/* Glassmorphism Cards */
.stMetric {
    background: white;
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    border: 1px solid #E2E8F0;
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

/* Primary Button Styling */
div.stButton > button {
    background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
    color: white !important;
    font-weight: 600;
    border-radius: 8px;
    border: none;
    padding: 0.6rem 1.2rem;
    box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
    transition: all 0.3s ease;
    width: 100%;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3);
    background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%);
}

/* Success Button Styling (Orange for convert) */
.btn-convert > div.stButton > button {
    background: linear-gradient(135deg, #F97316 0%, #EA580C 100%);
    box-shadow: 0 4px 6px -1px rgba(249, 115, 22, 0.2);
}

/* Download Button Specific */
div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
    box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.2);
    width: 100%;
}

/* Radio buttons container */
[data-testid="stRadio"] {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    border: 1px solid #E2E8F0;
}

/* File Uploader Dropzone */
[data-testid="stFileUploadDropzone"] {
    background: white;
    border: 2px dashed #CBD5E1;
    border-radius: 12px;
}

.metric-container {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 2rem;
}

.metric-card {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    flex: 1;
    text-align: center;
}

.metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #4F46E5;
}

.metric-label {
    font-size: 0.8rem;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title("📄 Document Master Ultra")
st.markdown("A suíte definitiva para processamento de documentos. Converta, otimize e renderize com precisão cirúrgica.")

st.divider()

# Instancia a engine principal
markdownify = Markdownify()

# Seleção principal da ferramenta
opcao = st.sidebar.radio(
    "Menu de Ferramentas",
    ("Extrair para Markdown", "Gerar PDF", "Otimizar & Comprimir PDF"),
    index=0
)

st.sidebar.divider()
st.sidebar.caption("v2.1 - Powered by PyMuPDF & WeasyPrint")

if opcao == "Extrair para Markdown":
    st.subheader("📄 Extrair Markdown de um Documento")
    st.markdown("Transforme PDFs, docs e outros arquivos em texto formatado `.md` otimizado para LLMs.")
    
    uploaded_file = st.file_uploader(
        "Upload do documento", 
        type=["pdf", "docx", "doc", "xlsx", "pptx", "html"]
    )
    
    if uploaded_file :
        st.info(f"Arquivo: **{uploaded_file.name}** ({format_size(len(uploaded_file.getvalue()))})")
        
        col1, col2 = st.columns(2)
        with col1:
            modo_imagem = st.radio(
                "Inclusão de Mídia:",
                ("Com imagens", "Somente texto"),
                help="Escolha 'Somente texto' para economizar tokens em LLMs."
            )
        
        embed_images = modo_imagem == "Com imagens"
        
        st.markdown('<div class="btn-convert">', unsafe_allow_html=True)
        if st.button("🚀 Iniciar Extração Profunda", type="primary"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
                
            try:
                with st.spinner("Analisando estrutura e extraindo conteúdo..."):
                    start_time = time.time()
                    md_content = markdownify.from_file(tmp_path, embed_images=embed_images)
                    elapsed = time.time() - start_time
                    
                st.success(f"✅ Extração finalizada em {elapsed:.1f}s")
                
                st.download_button(
                    label="📥 Baixar Markdown (.md)",
                    data=md_content,
                    file_name=f"{os.path.splitext(uploaded_file.name)[0]}.md",
                    mime="text/markdown"
                )
                
                with st.expander("👀 Visualizar Conteúdo"):
                    st.markdown(md_content, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erro: {e}")
            finally:
                if os.path.exists(tmp_path): os.remove(tmp_path)
        st.markdown('</div>', unsafe_allow_html=True)

elif opcao == "Gerar PDF":
    st.subheader("📝 Renderizar PDF Profissional")
    st.markdown("Converta seus arquivos Markdown em PDFs com estilo premium GitHub.")
    
    uploaded_md = st.file_uploader("Upload do arquivo .md", type=["md", "markdown", "txt"])
    
    if uploaded_md :
        if st.button("📄 Gerar PDF Estilizado", type="primary"):
            try:
                md_text = uploaded_md.getvalue().decode("utf-8")
                with st.spinner("Renderizando layout e estilos..."):
                    pdf_bytes = markdownify.to_pdf(md_text)
                
                st.success("✅ PDF gerado com sucesso!")
                st.download_button(
                    label="📥 Baixar PDF Gerado",
                    data=pdf_bytes,
                    file_name=f"{os.path.splitext(uploaded_md.name)[0]}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Erro: {e}")

elif opcao == "Otimizar & Comprimir PDF":
    st.subheader("⚡ Otimizador Inteligente de PDF")
    st.markdown("Reduza o tamanho dos seus arquivos PDF sem perder a qualidade visual de forma significativa.")
    
    uploaded_pdf = st.file_uploader("Upload do PDF para compressão", type=["pdf"])
    
    if uploaded_pdf:
        orig_size = len(uploaded_pdf.getvalue())
        st.info(f"Arquivo: **{uploaded_pdf.name}** | Tamanho original: **{format_size(orig_size)}**")
        
        col1, col2 = st.columns(2)
        with col1:
            metodo = st.selectbox(
                "Estratégia de Compressão",
                ["Simples (Preserva Texto)", "Agressiva (Rasterização)"],
                help="O modo simples limpa objetos duplicados e metadados. O agressivo converte páginas em imagens otimizadas."
            )
        with col2:
            qualidade = st.slider("Qualidade Visual", 10, 100, 85, help="Utilizado apenas no modo agressivo.")
            
        if metodo == "Agressiva (Rasterização)":
            dpi = st.select_slider("Resolução (DPI)", options=[72, 100, 150, 200, 300], value=150)
        else:
            dpi = 150

        if st.button("⚡ Otimizar Agora", type="primary"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_pdf.getvalue())
                tmp_path = tmp.name
            
            try:
                method_code = "simple" if "Simples" in metodo else "raster"
                
                with st.spinner("Executando algoritmos de otimização..."):
                    compressed_bytes, reduction = markdownify.optimize_pdf(
                        tmp_path, 
                        method=method_code, 
                        quality=qualidade, 
                        dpi=dpi
                    )
                
                new_size = len(compressed_bytes)
                
                # App Show Analytics
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-card">
                        <div class="metric-label">Original</div>
                        <div class="metric-value">{format_size(orig_size)}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Reduzido</div>
                        <div class="metric-value">{format_size(new_size)}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Economia</div>
                        <div class="metric-value" style="color: #10B981;">{reduction:.1f}%</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if reduction > 0:
                    st.success(f"✅ Sucesso! O arquivo foi reduzido em {format_size(orig_size - new_size)}.")
                else:
                    st.warning("⚠️ O arquivo já estava otimizado ao máximo. Nenhuma redução adicional foi possível.")

                st.download_button(
                    label="📥 Baixar PDF Otimizado",
                    data=compressed_bytes,
                    file_name=f"{os.path.splitext(uploaded_pdf.name)[0]}_otimizado.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Erro na compressão: {e}")
            finally:
                if os.path.exists(tmp_path): os.remove(tmp_path)
