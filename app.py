import streamlit as st
import os
import tempfile
import time
from leitor_pdf import Markdownify
from core import format_size

# Configuração da página com tema light forçado e layout wide
st.set_page_config(
    page_title="Document Master Ultra | Pro", 
    page_icon="📄", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Design System: UI/UX Pro Max Edition (Fundo Branco + Indigo/Slate)
design_system_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&display=swap');

/* Reset e Base */
:root {
    --primary: #4F46E5;
    --primary-hover: #4338CA;
    --bg-white: #FFFFFF;
    --bg-slate-50: #F8FAFC;
    --text-slate-900: #0F172A;
    --text-slate-600: #475569;
    --border-slate-200: #E2E8F0;
    --emerald-500: #10B981;
    --amber-500: #F59E0B;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--text-slate-900);
    background-color: var(--bg-white);
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: var(--bg-slate-50);
    border-right: 1px solid var(--border-slate-200);
}

[data-testid="stSidebar"] .stRadio > label {
    font-weight: 600;
    color: var(--text-slate-900);
    margin-bottom: 15px;
}

/* Main Title Styling */
.main-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 800;
    font-size: 2.5rem;
    color: var(--text-slate-900);
    letter-spacing: -0.04em;
    margin-bottom: 0.5rem;
}

.sub-title {
    color: var(--text-slate-600);
    font-size: 1.1rem;
    margin-bottom: 2rem;
}

/* Professional Cards (Containers) */
[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid var(--border-slate-200) !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    background-color: var(--bg-white) !important;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.03) !important;
}

/* Custom Metric Cards for Optimizer */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}

.pro-metric {
    padding: 1.25rem;
    background: var(--bg-slate-50);
    border: 1px solid var(--border-slate-200);
    border-radius: 12px;
    text-align: center;
}

.pro-metric-val {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary);
}

.pro-metric-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-slate-600);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Button UI Pro */
div.stButton > button {
    background-color: var(--primary);
    color: white !important;
    border-radius: 10px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    border: none;
    transition: all 0.2s ease-in-out;
    box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.1);
}

div.stButton > button:hover {
    background-color: var(--primary-hover);
    transform: translateY(-1px);
    box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.2);
}

/* Success Download Button */
div[data-testid="stDownloadButton"] > button {
    background-color: var(--emerald-500);
    width: 100%;
}

/* Form Helper Text */
.stMarkdown p {
    line-height: 1.6;
}

/* Divider Styling */
hr {
    margin: 2rem 0 !important;
    border-color: var(--border-slate-200) !important;
}
</style>
"""
st.markdown(design_system_css, unsafe_allow_html=True)

# App Logic initialization
markdownify = Markdownify()

# --- SIDEBAR NAV ---
with st.sidebar:
    st.markdown('<p style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 1.5rem; font-weight: 800; margin-bottom: 0;">Master Ultra</p>', unsafe_allow_html=True)
    st.caption("v2.5 — UI-UX Pro Edition")
    st.divider()
    
    selected = st.radio(
        "Navegação Principal",
        ["📦 Converter Documentos", "⚡ Otimizar PDFs", "📄 Markdown para PDF"],
        index=0
    )
    
    st.divider()
    st.caption("Desenvolvido por Kristiano Plácido")

# --- MAIN PAGE HEADER ---
col_header_1, col_header_2 = st.columns([2, 1])
with col_header_1:
    st.markdown('<p class="main-title">A Inteligência em Documentos.</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Converta, otimize e estruture arquivos para o futuro da IA.</p>', unsafe_allow_html=True)

# --- WORKSPACE AREA ---
if selected == "📦 Converter Documentos":
    with st.container(border=True):
        st.subheader("Extração Universal para Markdown")
        st.write("Suporta PDF, DOCX, XLSX, PPTX e HTML. Otimizado para alta fidelidade e leitura por LLMs.")
        
        file = st.file_uploader("Arraste seu arquivo aqui", type=["pdf", "docx", "doc", "xlsx", "pptx", "html"], key="uploader_conv")
        
        if file:
            c1, c2 = st.columns([3, 1])
            with c1:
                st.info(f"**{file.name}** pronto para processamento. ({format_size(len(file.getvalue()))})")
            with c2:
                mode = st.toggle("Incluir Imagens", value=True, help="Embutir imagens em base64 no Markdown.")
            
            if st.button("🚀 Iniciar Conversão Inteligente", use_container_width=True):
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as tmp:
                    tmp.write(file.getvalue())
                    tmp_path = tmp.name
                
                try:
                    with st.status("Extraindo conteúdo e preservando layout...", expanded=True) as status:
                        start = time.time()
                        md = markdownify.from_file(tmp_path, embed_images=mode)
                        elapsed = time.time() - start
                        status.update(label=f"Concluído em {elapsed:.1f}s!", state="complete", expanded=False)
                    
                    st.success("Markdown gerado com sucesso.")
                    st.download_button("📥 Baixar Arquivo .md", md, file_name=f"{os.path.splitext(file.name)[0]}.md")
                    
                    with st.expander("👀 Preview do Documento"):
                        st.markdown(md, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erro na extração: {e}")
                finally:
                    if os.path.exists(tmp_path): os.remove(tmp_path)

elif selected == "⚡ Otimizar PDFs":
    with st.container(border=True):
        st.subheader("Otimização Estrutural & Raster")
        st.write("Reduza o tamanho de PDFs para armazenamento ou envio, escolhendo entre preservação de texto ou compressão agressiva.")
        
        file_opt = st.file_uploader("Selecione o PDF para otimizar", type=["pdf"], key="uploader_opt")
        
        if file_opt:
            orig_bytes = file_opt.getvalue()
            st.info(f"PDF carregado: **{file_opt.name}** ({format_size(len(orig_bytes))})")
            
            col_opt_1, col_opt_2 = st.columns(2)
            with col_opt_1:
                strat = st.selectbox("Estratégia", ["Simples (Preservar Texto)", "Agressiva (Converter para Imagem)"])
            with col_opt_2:
                qual = st.slider("Qualidade Visual", 10, 100, 85)
                if "Agressiva" in strat:
                    dpi = st.select_slider("Resolução (DPI)", options=[72, 100, 150, 200, 300], value=150)
                else:
                    dpi = 150
            
            if st.button("⚡ Executar Otimização"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(orig_bytes)
                    tmp_path = tmp.name
                
                try:
                    with st.spinner("Compactando dados estruturais..."):
                        m_code = "simple" if "Simples" in strat else "raster"
                        compressed, reduction = markdownify.optimize_pdf(tmp_path, method=m_code, quality=qual, dpi=dpi)
                    
                    # Dashboard de Resultado Pro
                    st.markdown(f"""
                    <div class="metrics-grid">
                        <div class="pro-metric">
                            <p class="pro-metric-label">Original</p>
                            <p class="pro-metric-val">{format_size(len(orig_bytes))}</p>
                        </div>
                        <div class="pro-metric">
                            <p class="pro-metric-label">Otimizado</p>
                            <p class="pro-metric-val">{format_size(len(compressed))}</p>
                        </div>
                        <div class="pro-metric">
                            <p class="pro-metric-label">Economia</p>
                            <p class="pro-metric-val" style="color: var(--emerald-500);">{reduction:.1f}%</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.download_button("📥 Baixar PDF Otimizado", compressed, file_name=f"{os.path.splitext(file_opt.name)[0]}_opt.pdf")
                except Exception as e:
                    st.error(f"Erro: {e}")
                finally:
                    if os.path.exists(tmp_path): os.remove(tmp_path)

elif selected == "📄 Markdown para PDF":
    with st.container(border=True):
        st.subheader("Renderizador Profissional WeasyPrint")
        st.write("Converta documentos Markdown em PDFs elegantes com suporte a tabelas e imagens.")
        
        file_md = st.file_uploader("Upload do arquivo .md", type=["md", "markdown", "txt"], key="uploader_md")
        
        if file_md:
            if st.button("📄 Gerar PDF Master"):
                try:
                    text = file_md.getvalue().decode("utf-8")
                    with st.spinner("Desenhando PDF com CSS GitHub..."):
                        pdf = markdownify.to_pdf(text)
                    st.success("Renderização concluída.")
                    st.download_button("📥 Baixar PDF Renderizado", pdf, file_name=f"documento_renderizado.pdf")
                except Exception as e:
                    st.error(f"Erro: {e}")

# --- FOOTEER ---
st.divider()
f_col1, f_col2 = st.columns([3, 1])
with f_col2:
    st.caption("© 2024 Document Master Ultra — Kristiano Plácido")
