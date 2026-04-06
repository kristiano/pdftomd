import streamlit as st
import os
import tempfile
import time
from leitor_pdf import Markdownify
from core import format_size

# Configuração da página - Canivete Suíço
st.set_page_config(
    page_title="Canivete suíço para documentos | Pro", 
    page_icon="📄", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SISTEMA DE SESSÃO ---
if 'engine' not in st.session_state:
    st.session_state.engine = Markdownify()

# Design System: Sidebar Escura + Conteúdo Claro (ECharts Theme)
design_system_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&display=swap');

/* Main Content (Branco) */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #FFFFFF !important;
}

[data-testid="stHeader"] {
    background-color: transparent !important;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #0F172A !important;
}

/* Sidebar ESTILIZADA ESCURA (Fixo) */
[data-testid="stSidebar"] {
    background-color: #0B1120 !important;
    border-right: 1px solid #1E293B !important;
    color: #F8FAFC !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #F8FAFC !important;
}

[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
}

/* Estilo do Selectbox na Sidebar Escura */
[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
    background-color: #1E293B !important;
    color: white !important;
    border: 1px solid #334155 !important;
}

/* Typography Main */
.main-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 800;
    font-size: 2.8rem;
    color: #0F172A;
    letter-spacing: -0.04em;
}

.sub-title {
    color: #475569;
    font-size: 1.15rem;
    margin-bottom: 2.5rem;
}

/* Cards (Conteúdo Principal) */
[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #E2E8F0 !important;
    border-radius: 20px !important;
    padding: 2.5rem !important;
    background-color: #FFFFFF !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
}

/* Metrics Grid */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    margin: 2rem 0;
}

.pro-metric {
    padding: 1.5rem;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    text-align: center;
}

.pro-metric-val {
    font-size: 1.8rem;
    font-weight: 800;
    color: #4F46E5;
}

/* Buttons */
div.stButton > button {
    background-color: #4F46E5 !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 0.8rem 2rem !important;
    font-weight: 600 !important;
    border: none !important;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    background-color: #4338CA !important;
    transform: scale(1.01);
}

div[data-testid="stDownloadButton"] > button {
    background-color: #10B981 !important;
}

/* Cancel Button específico */
.cancel-btn > div.stButton > button {
    background-color: #EF4444 !important;
}
</style>
"""
st.markdown(design_system_css, unsafe_allow_html=True)

markdownify = st.session_state.engine

# --- SIDEBAR (Estilo ECharts Dark) ---
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 25px;">
            <div style="background-color: #4F46E5; width: 42px; height: 42px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 12px;">
                <span style="color: white; font-size: 22px; font-weight: bold;">C</span>
            </div>
            <div>
                <h2 style="margin: 0; font-size: 1.25rem; font-weight: 800; color: white;">Canivete Suíço</h2>
                <p style="margin: 0; font-size: 0.75rem; color: #94A3B8;">v2.5 — Remodelador de docs</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("<h3 style='color: white; font-size: 1rem; margin-bottom: 10px;'>🛠️ Ferramentas</h3>", unsafe_allow_html=True)
    selected = st.selectbox(
        "Operação",
        ["📦 Converter Documentos", "⚡ Otimizar PDFs", "📄 Markdown para PDF"],
        index=0,
        label_visibility="collapsed"
    )
    
    # Espaçador dinâmico para o botão de cancelar
    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
    cancel_placeholder = st.empty()
    
    st.divider()
    
    st.markdown("""
        <div style="padding: 12px; border-radius: 10px; background-color: rgba(79, 70, 229, 0.1); border: 1px solid rgba(79, 70, 229, 0.2);">
            <p style="margin: 0; font-size: 0.7rem; color: #818CF8; font-weight: 600; text-transform: uppercase;">Desenvolvido por</p>
            <p style="margin: 0; font-size: 0.9rem; font-weight: 700; color: white;">Kristiano Plácido</p>
        </div>
    """, unsafe_allow_html=True)

# --- CONTEÚDO PRINCIPAL ---
st.markdown('<p class="main-title">A Inteligência em Documentos.</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Converta, otimize e estruture arquivos para o futuro da IA.</p>', unsafe_allow_html=True)

if selected == "📦 Converter Documentos":
    with st.container(border=True):
        st.subheader("Extração Universal para Markdown")
        st.write("Suporta PDF, DOCX, XLSX, PPTX e HTML. Otimizado para alta fidelidade e leitura por LLMs.")
        
        file = st.file_uploader("Upload", type=["pdf", "docx", "doc", "xlsx", "pptx", "html"], label_visibility="collapsed")
        
        if file:
            c1, c2 = st.columns([3, 1])
            with c1: st.info(f"**{file.name}** ({format_size(len(file.getvalue()))})")
            with c2: mode = st.toggle("Incluir Imagens", value=True)
            
            if st.button("🚀 Iniciar Conversão"):
                p_bar = st.progress(0, "Preparando extração...")
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as tmp:
                    tmp.write(file.getvalue()); tmp_path = tmp.name
                try:
                    p_bar.progress(30, "Extraindo dados...")
                    md = markdownify.from_file(tmp_path, embed_images=mode)
                    p_bar.progress(100, "Concluído!"); time.sleep(0.5); p_bar.empty()
                    st.success("Sucesso!"); st.download_button("📥 Baixar .md", md, file_name=f"{os.path.splitext(file.name)[0]}.md")
                except Exception as e: st.error(f"Erro: {e}")
                finally:
                    if os.path.exists(tmp_path): os.remove(tmp_path)

elif selected == "⚡ Otimizar PDFs":
    with st.container(border=True):
        st.subheader("Otimização Inteligente")
        st.write("Reduza o tamanho de PDFs para armazenamento ou envio.")
        
        file_opt = st.file_uploader("PDF", type=["pdf"], key="uploader_opt", label_visibility="collapsed")
        
        if file_opt:
            orig_bytes = file_opt.getvalue()
            st.info(f"PDF carregado: **{file_opt.name}** ({format_size(len(orig_bytes))})")
            
            col_opt_1, col_opt_2 = st.columns(2)
            with col_opt_1: strat = st.selectbox("Estratégia", ["Simples (Preservar Texto)", "Agressiva (Rasterizar)"])
            with col_opt_2:
                qual = st.slider("Qualidade Visual", 10, 100, 85)
                dpi = st.select_slider("Resolução (DPI)", options=[72, 100, 150, 200, 300], value=150) if "Agressiva" in strat else 150
            
            if st.button("⚡ Executar Otimização", type="primary"):
                start_time = time.time()
                with cancel_placeholder.container():
                     st.markdown('<div class="cancel-btn">', unsafe_allow_html=True)
                     if st.button("❌ Cancelar"): st.rerun()
                     st.markdown('</div>', unsafe_allow_html=True)
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(orig_bytes); tmp_path = tmp.name
                
                try:
                    p_ui = st.progress(0, "Iniciando motor...")
                    m_code = "simple" if "Simples" in strat else "raster"
                    def callback(p, t):
                        elapsed = time.time() - start_time
                        eta = int((elapsed / p) - elapsed) if p > 0.05 else 0
                        p_ui.progress(p, text=f"**{int(p*100)}%** • {t} {'| ETA: ~'+str(eta)+'s' if eta > 0 else ''}")
                        return False
                    
                    compressed, reduction, was_cancelled = markdownify.optimize_pdf(tmp_path, method=m_code, quality=qual, dpi=dpi, progress_callback=callback)
                    p_ui.empty(); cancel_placeholder.empty()
                    
                    if not was_cancelled:
                        st.markdown(f"""
                        <div class="metrics-grid">
                            <div class="pro-metric"><p style="font-size:0.75rem; color:#64748B; margin:0;">ORIGINAL</p><p class="pro-metric-val">{format_size(len(orig_bytes))}</p></div>
                            <div class="pro-metric"><p style="font-size:0.75rem; color:#64748B; margin:0;">OTIMIZADO</p><p class="pro-metric-val">{format_size(len(compressed))}</p></div>
                            <div class="pro-metric"><p style="font-size:0.75rem; color:#64748B; margin:0;">ECONOMIA</p><p class="pro-metric-val" style="color: #10B981;">{reduction:.1f}%</p></div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.download_button("📥 Baixar PDF Otimizado", compressed, file_name=f"{os.path.splitext(file_opt.name)[0]}_opt.pdf")
                except Exception as e: st.error(f"Erro: {e}")
                finally:
                    if os.path.exists(tmp_path): os.remove(tmp_path)

elif selected == "📄 Markdown para PDF":
    with st.container(border=True):
        st.subheader("Renderizador Profissional")
        st.write("Converta documentos Markdown em PDFs elegantes.")
        
        file_md = st.file_uploader("Upload do arquivo .md", type=["md", "markdown", "txt"], label_visibility="collapsed")
        
        if file_md:
            if st.button("📄 Gerar PDF Master"):
                try:
                    text = file_md.getvalue().decode("utf-8")
                    with st.spinner("Desenhando PDF..."):
                        pdf = markdownify.to_pdf(text)
                    st.success("Pronto!"); st.download_button("📥 Baixar PDF", pdf, file_name=f"documento_renderizado.pdf")
                except Exception as e: st.error(f"Erro: {e}")

# --- FOOTEER ---
st.divider()
st.caption("© 2024 canivete suíço para documentos — Kristiano Plácido")
