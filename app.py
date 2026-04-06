import streamlit as st
import os
import tempfile
import time
import threading
import queue
from leitor_pdf import Markdownify
from core import format_size

# Configuração da página - Canivete Suíço
st.set_page_config(
    page_title="Canivete suíço para documentos | Pro", 
    page_icon="📄", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SISTEMA DE SESSÃO CORPORATIVO ---
if 'engine' not in st.session_state:
    st.session_state.engine = Markdownify()

if 'stop_event' not in st.session_state:
    st.session_state.stop_event = threading.Event()

# Função de callback para o botão Cancelar (Executa ANTES de qualquer renderização)
def on_cancel():
    st.session_state.stop_event.set()

# Design System: ECharts Clean Light Theme
design_system_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&display=swap');

html, body, [data-testid="stAppViewContainer"] { background-color: #FFFFFF !important; }
[data-testid="stHeader"] { background-color: transparent !important; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #1E293B !important; }

/* Sidebar Clean Light */
[data-testid="stSidebar"] {
    background-color: #F8FAFC !important;
    border-right: 1px solid #E2E8F0 !important;
}

.main-title { font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 2.8rem; color: #0F172A; letter-spacing: -0.04em; }
.sub-title { color: #64748B; font-size: 1.1rem; margin-bottom: 2.5rem; }

[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px !important;
    padding: 2.5rem !important;
    background-color: #FFFFFF !important;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.04) !important;
}

/* --- BOTÕES PADRONIZADOS E ALINHADOS --- */
div.stButton > button {
    height: 3.2rem !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
}

/* Botão Primário (Indigo) */
div.stButton > button[kind="primary"], div.stButton > button:not([kind="secondary"]):not([aria-label*="Cancelar"]) {
    background-color: #4F46E5 !important;
    color: white !important;
}
div.stButton > button:not([aria-label*="Cancelar"]):hover {
    background-color: #4338CA !important;
}

/* Botão Cancelar (Alinhado via Atributo CSS) */
/* Alvo específico para botões que contém "Cancelar" no texto/aria-label */
div[data-testid="stButton"] button[aria-label*="Cancelar"], 
div[data-testid="stButton"] button:has(div:contains("Cancelar")) {
    background-color: #FFFFFF !important;
    color: #EF4444 !important;
    border: 1px solid #FECACA !important;
    padding: 0 15px !important;
}
div[data-testid="stButton"] button[aria-label*="Cancelar"]:hover {
    background-color: #FEF2F2 !important;
    border-color: #EF4444 !important;
}

/* Metrics Grid */
.metrics-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin: 2rem 0; }
.pro-metric { padding: 1.5rem; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; text-align: center; }
.pro-metric-val { font-size: 1.8rem; font-weight: 800; color: #4F46E5; }

div[data-testid="stDownloadButton"] > button { background-color: #10B981 !important; color: white !important; }
</style>
"""
st.markdown(design_system_css, unsafe_allow_html=True)

markdownify = st.session_state.engine

# Helper Assíncrono com Correção de Argumentos
def run_async(method, stop_event, *args, **kwargs):
    q = queue.Queue()
    stop_event.clear()
    def wrapper():
        try:
            def cb(p, t): 
                q.put({"type": "p", "v": p, "t": t})
                return stop_event.is_set()
            kwargs["progress_callback"] = cb
            res = method(*args, **kwargs)
            if stop_event.is_set(): q.put({"type": "c"})
            elif isinstance(res, tuple): q.put({"type": "r", "val": res[0], "red": res[1], "c": res[2]})
            else: q.put({"type": "r", "val": res})
        except Exception as e: q.put({"type": "e", "m": str(e)})
    threading.Thread(target=wrapper, daemon=True).start()
    return q

def show_progress(q, start):
    p_ui = st.empty()
    while True:
        try:
            msg = q.get(timeout=0.2)
            if msg["type"] == "p":
                elap = time.time() - start
                eta = int((elap / msg["v"]) - elap) if msg["v"] > 0.05 else 0
                eta_txt = f"| ETA: ~{eta}s" if eta > 0 else "| Finalizando..."
                p_ui.progress(msg["v"], text=f"**{int(msg['v']*100)}%** • {msg['t']} {eta_txt}")
            elif msg["type"] == "r": p_ui.empty(); return msg
            elif msg["type"] == "c": p_ui.empty(); st.warning("Ação cancelada."); return None
            elif msg["type"] == "e": p_ui.empty(); st.error(f"Erro: {msg['m']}"); return None
        except queue.Empty: time.sleep(0.08)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## Canivete Suíço")
    st.divider()
    selected = st.selectbox("Ferramenta", ["📦 Converter Documentos", "⚡ Otimizar PDFs", "📄 Markdown para PDF"], label_visibility="collapsed")
    st.divider()

# --- HEADER ---
st.markdown('<p class="main-title">A Inteligência em Documentos.</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Processamento profissional com interrupção instantânea.</p>', unsafe_allow_html=True)

if selected == "📦 Converter Documentos":
    with st.container(border=True):
        file = st.file_uploader("Upload", type=["pdf", "docx", "doc", "xlsx", "pptx", "html"], label_visibility="collapsed")
        if file:
            c1, c2 = st.columns([3, 1])
            with c1: st.info(f"**{file.name}** ({format_size(len(file.getvalue()))})")
            with c2: mode = st.toggle("Imagens", value=True)
            
            # ALINHAMENTO PERFEITO SEM DIVS WRAPPERS (Melhora o Flexbox do Streamlit)
            col_b1, col_b2 = st.columns([2, 1])
            btn_run = col_b1.button("🚀 Iniciar Conversão", type="primary", use_container_width=True)
            # USANDO ON_CLICK PARA CANCELAMENTO INSTANTÂNEO
            col_b2.button("❌ Cancelar", key="cancel_conv", on_click=on_cancel, use_container_width=True)
            
            if btn_run:
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as tmp:
                    tmp.write(file.getvalue()); tp = tmp.name
                try:
                    res = show_progress(run_async(markdownify.from_file, st.session_state.stop_event, tp, embed_images=mode), time.time())
                    if res and "val" in res:
                        st.success("Pronto!"); st.download_button("📥 Baixar .md", res["val"], file_name=f"{os.path.splitext(file.name)[0]}.md")
                        with st.expander("👀 Preview", expanded=True): st.markdown(res["val"], unsafe_allow_html=True)
                finally:
                    if os.path.exists(tp): os.remove(tp)

elif selected == "⚡ Otimizar PDFs":
    with st.container(border=True):
        file_opt = st.file_uploader("PDF", type=["pdf"], key="uploader_opt", label_visibility="collapsed")
        if file_opt:
            orig = file_opt.getvalue()
            st.info(f"**{file_opt.name}** ({format_size(len(orig))})")
            co1, co2 = st.columns(2)
            with co1: strat = st.selectbox("Estratégia", ["Simples", "Agressiva"])
            with co2:
                qual = st.slider("Qualidade", 10, 100, 85)
                dpi = st.select_slider("Resol.", options=[72, 100, 150, 200, 300], value=150) if "Agressiva" in strat else 150
            
            col_b1, col_b2 = st.columns([2, 1])
            btn_run = col_b1.button("⚡ Executar Otimização", type="primary", use_container_width=True)
            col_b2.button("❌ Cancelar", key="cancel_opt", on_click=on_cancel, use_container_width=True)
            
            if btn_run:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(orig); tp = tmp.name
                try:
                    m = "simple" if "Simples" in strat else "raster"
                    res = show_progress(run_async(markdownify.optimize_pdf, st.session_state.stop_event, tp, method=m, quality=qual, dpi=dpi), time.time())
                    if res and not res.get("c", False):
                        st.markdown(f"""<div class="metrics-grid">
                            <div class="pro-metric"><p style="font-size:0.7rem; color:#64748B; margin:0;">ORIGINAL</p><p class="pro-metric-val">{format_size(len(orig))}</p></div>
                            <div class="pro-metric"><p style="font-size:0.7rem; color:#64748B; margin:0;">OTIMIZADO</p><p class="pro-metric-val">{format_size(len(res['val']))}</p></div>
                            <div class="pro-metric"><p style="font-size:0.7rem; color:#64748B; margin:0;">ECONOMIA</p><p class="pro-metric-val" style="color:#10B981;">{res['red']:.1f}%</p></div>
                        </div>""", unsafe_allow_html=True)
                        st.download_button("📥 Baixar PDF", res["val"], file_name=f"{os.path.splitext(file_opt.name)[0]}_opt.pdf")
                finally:
                    if os.path.exists(tp): os.remove(tp)

elif selected == "📄 Markdown para PDF":
    with st.container(border=True):
        file_md = st.file_uploader("Markdown", type=["md", "txt"], label_visibility="collapsed")
        if file_md:
            col_b1, col_b2 = st.columns([2, 1])
            btn_run = col_b1.button("📄 Gerar PDF Renderizado", type="primary", use_container_width=True)
            col_b2.button("❌ Cancelar", key="cancel_md", on_click=on_cancel, use_container_width=True)
            if btn_run:
                try:
                    text = file_md.getvalue().decode("utf-8")
                    res = show_progress(run_async(markdownify.to_pdf, st.session_state.stop_event, text), time.time())
                    if res: st.success("Renderizado!"); st.download_button("📥 Baixar .pdf", res["val"], file_name="doc.pdf")
                except Exception as e: st.error(f"Erro: {e}")

st.divider()
st.caption("© 2024 canivete suíço para documentos — Kristiano Plácido")
