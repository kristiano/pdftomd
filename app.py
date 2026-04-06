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

# --- SISTEMA DE SESSÃO E CONCORRÊNCIA ---
# Instanciar a engine por sessão para garantir independência entre usuários simultâneos
if 'engine' not in st.session_state:
    st.session_state.engine = Markdownify()

if 'dark_mode' not in st.session_state: st.session_state.dark_mode = False
if 'is_processing' not in st.session_state: st.session_state.is_processing = False

# Sidebar (Design ECharts)
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="background-color: #4F46E5; width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 12px;">
                <span style="color: white; font-size: 20px; font-weight: bold;">C</span>
            </div>
            <div>
                <h2 style="margin: 0; font-size: 1.2rem; font-weight: 800;">Canivete Suíço</h2>
                <p style="margin: 0; font-size: 0.75rem; color: #64748B;">v2.5 — Remodelador de docs</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("### 🛠️ Ferramentas")
    selected = st.selectbox("Operação", ["📦 Converter Documentos", "⚡ Otimizar PDFs", "📄 Markdown para PDF"], index=0, label_visibility="collapsed")
    st.divider()
    st.markdown("### ⚙️ Ajustes")
    st.session_state.dark_mode = st.toggle("🌙 Modo Escuro", value=st.session_state.dark_mode)
    cancel_placeholder = st.empty()
    st.divider()
    st.markdown("""
        <div style="padding: 10px; border-radius: 8px; background-color: rgba(79, 70, 229, 0.05); border: 1px solid rgba(79, 70, 229, 0.1);">
            <p style="margin: 0; font-size: 0.75rem; color: #4F46E5; font-weight: 600;">Desenvolvido por</p>
            <p style="margin: 0; font-size: 0.85rem; font-weight: 700;">Kristiano Plácido</p>
        </div>
    """, unsafe_allow_html=True)

# Theme CSS Variables
if st.session_state.dark_mode:
    primary = "#818CF8"; primary_hover = "#6366F1"; bg_main = "#0F172A"; bg_card = "#1E293B"
    bg_sidebar = "#0B1120"; text_main = "#F8FAFC"; text_sub = "#94A3B8"; border = "#334155"; metric_bg = "#334155"
else:
    primary = "#4F46E5"; primary_hover = "#4338CA"; bg_main = "#FFFFFF"; bg_card = "#FFFFFF"
    bg_sidebar = "#F8FAFC"; text_main = "#0F172A"; text_sub = "#475569"; border = "#E2E8F0"; metric_bg = "#F8FAFC"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&display=swap');
html, body, [data-testid="stAppViewContainer"] {{ background-color: {bg_main} !important; }}
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; color: {text_main} !important; }}
[data-testid="stSidebar"] {{ background-color: {bg_sidebar} !important; border-right: 1px solid {border} !important; }}
.main-title {{ font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 2.8rem; letter-spacing: -0.04em; }}
.sub-title {{ color: {text_sub}; font-size: 1.15rem; margin-bottom: 2.5rem; }}
[data-testid="stVerticalBlockBorderWrapper"] {{ border: 1px solid {border} !important; border-radius: 20px !important; padding: 2.5rem !important; background-color: {bg_card} !important; }}
.metrics-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin: 2rem 0; }}
.pro-metric {{ padding: 1.5rem; background: {metric_bg}; border: 1px solid {border}; border-radius: 16px; text-align: center; }}
.pro-metric-val {{ font-size: 1.8rem; font-weight: 800; color: {primary}; }}
div.stButton > button {{ background-color: {primary} !important; color: white !important; border-radius: 12px !important; font-weight: 600 !important; width: 100%; }}
div[data-testid="stDownloadButton"] > button {{ background-color: #10B981 !important; }}
.cancel-btn > div.stButton > button {{ background-color: #EF4444 !important; }}
</style>
""", unsafe_allow_html=True)

# Engine individual por usuário
markdownify = st.session_state.engine

st.markdown('<p class="main-title">A Inteligência em Documentos.</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">Converta, otimize e estruture arquivos para o futuro da IA.</p>', unsafe_allow_html=True)

# Workspace
if selected == "📦 Converter Documentos":
    with st.container(border=True):
        st.subheader("Extração Universal para Markdown")
        file = st.file_uploader("Upload", type=["pdf", "docx", "doc", "xlsx", "pptx", "html"], label_visibility="collapsed")
        if file:
            c1, c2 = st.columns([3, 1])
            with c1: st.info(f"**{file.name}** ({format_size(len(file.getvalue()))})")
            with c2: mode = st.toggle("Imagens", value=True)
            if st.button("🚀 Iniciar Conversão"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as tmp:
                    tmp.write(file.getvalue()); tmp_path = tmp.name
                try:
                    p = st.progress(0, "Iniciando processamento...")
                    md = markdownify.from_file(tmp_path, embed_images=mode)
                    p.progress(100, "Concluído!"); time.sleep(0.5); p.empty()
                    st.success("Sucesso!"); st.download_button("📥 Baixar .md", md, file_name=f"{os.path.splitext(file.name)[0]}.md")
                except Exception as e: st.error(f"Erro na extração: {e}")
                finally:
                    if os.path.exists(tmp_path): os.remove(tmp_path)

elif selected == "⚡ Otimizar PDFs":
    with st.container(border=True):
        st.subheader("Otimização Inteligente")
        file_opt = st.file_uploader("PDF", type=["pdf"], label_visibility="collapsed")
        if file_opt:
            orig_bytes = file_opt.getvalue()
            st.info(f"**{file_opt.name}** ({format_size(len(orig_bytes))})")
            col1, col2 = st.columns(2)
            with col1: strat = st.selectbox("Estratégia", ["Simples (Preservar Texto)", "Agressiva (Rasterizar)"])
            with col2:
                qual = st.slider("Qualidade", 10, 100, 85)
                dpi = st.select_slider("DPI", options=[72, 100, 150, 200, 300], value=150) if "Agressiva" in strat else 150
            
            if st.button("⚡ Executar Otimização", type="primary"):
                st.session_state.is_processing = True
                start_time = time.time()
                with cancel_placeholder.container():
                     st.markdown('<div class="cancel-btn">', unsafe_allow_html=True)
                     if st.button("❌ Cancelar Operação"):
                         st.session_state.is_processing = False; st.rerun()
                     st.markdown('</div>', unsafe_allow_html=True)
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(orig_bytes); tmp_path = tmp.name
                
                try:
                    p_ui = st.progress(0, "Iniciando motor de otimização...")
                    m_code = "simple" if "Simples" in strat else "raster"
                    def callback(p, t):
                        elapsed = time.time() - start_time
                        eta_val = int((elapsed / p) - elapsed) if p > 0.05 else 0
                        eta_str = f"| ETA: ~{eta_val}s" if eta_val > 0 else ""
                        p_ui.progress(p, text=f"**{int(p*100)}%** • {t} {eta_str}")
                        return False
                    compressed, reduction, was_cancelled = markdownify.optimize_pdf(tmp_path, method=m_code, quality=qual, dpi=dpi, progress_callback=callback)
                    p_ui.empty(); cancel_placeholder.empty(); st.session_state.is_processing = False
                    
                    if not was_cancelled:
                        st.markdown(f"""
                        <div class="metrics-grid">
                            <div class="pro-metric" style="background: {metric_bg}; border-color: {border};"><p style="font-size:0.8rem; color:{text_sub}; margin:0;">ORIGINAL</p><p class="pro-metric-val">{format_size(len(orig_bytes))}</p></div>
                            <div class="pro-metric" style="background: {metric_bg}; border-color: {border};"><p style="font-size:0.8rem; color:{text_sub}; margin:0;">REDUZIDO</p><p class="pro-metric-val">{format_size(len(compressed))}</p></div>
                            <div class="pro-metric" style="background: {metric_bg}; border-color: {border};"><p style="font-size:0.8rem; color:{text_sub}; margin:0;">ECONOMIA</p><p class="pro-metric-val" style="color: #10B981;">{reduction:.1f}%</p></div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.download_button("📥 Baixar PDF Otimizado", compressed, file_name=f"{os.path.splitext(file_opt.name)[0]}_opt.pdf")
                except Exception as e:
                    p_ui.empty(); cancel_placeholder.empty(); st.error(f"Erro crítico: {e}")
                finally:
                    if os.path.exists(tmp_path): os.remove(tmp_path)

elif selected == "📄 Markdown para PDF":
    with st.container(border=True):
        st.subheader("Renderizador WeasyPrint")
        file_md = st.file_uploader("Arquivo", type=["md", "markdown", "txt"], label_visibility="collapsed")
        if file_md:
            if st.button("📄 Gerar PDF Master"):
                try:
                    text = file_md.getvalue().decode("utf-8")
                    with st.spinner("Renderizando..."): pdf = markdownify.to_pdf(text)
                    st.success("Pronto!"); st.download_button("📥 Baixar PDF", pdf, file_name=f"renderizado.pdf")
                except Exception as e: st.error(f"Erro: {e}")

# Footer
st.divider()
st.caption("© 2024 canivete suíço para documentos — Kristiano Plácido")
