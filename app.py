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

/* Sidebar */
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

/* Botões Padronizados Estilo Premium */
div.stButton > button {
    height: 3.2rem !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
    border: none !important;
}

div.stButton > button:not([aria-label*="Cancelar"]) {
    background-color: #4F46E5 !important;
    color: white !important;
}

div[data-testid="stButton"] button[aria-label*="Cancelar"] {
    background-color: #FFFFFF !important;
    color: #EF4444 !important;
    border: 1px solid #FECACA !important;
}

.metrics-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin: 2rem 0; }
.pro-metric { padding: 1.5rem; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; text-align: center; }
.pro-metric-val { font-size: 1.8rem; font-weight: 800; color: #4F46E5; }

div[data-testid="stDownloadButton"] > button { background-color: #10B981 !important; color: white !important; }
</style>
"""
st.markdown(design_system_css, unsafe_allow_html=True)

markdownify = st.session_state.engine

# Helper Assíncrono
def run_async(task_func, stop_event, *args, **kwargs):
    q = queue.Queue()
    stop_event.clear()
    def wrapper():
        try:
            def cb(p, t): 
                q.put({"type": "p", "v": p, "t": t})
                return stop_event.is_set()
            kwargs["progress_callback"] = cb
            res = task_func(*args, **kwargs)
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
                p_ui.progress(msg["v"], text=f"**{int(msg['v']*100)}%** • {msg['t']} {'| ETA: ~'+str(eta)+'s' if eta > 0 else ''}")
            elif msg["type"] == "r": p_ui.empty(); return msg
            elif msg["type"] == "c": p_ui.empty(); st.warning("Cancelado."); return None
            elif msg["type"] == "e": p_ui.empty(); st.error(f"Erro: {msg['m']}"); return None
        except queue.Empty: time.sleep(0.08)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## Canivete Suíço")
    st.divider()
    selected = st.selectbox("Ferramenta", ["📦 Converter Documentos", "⚡ Otimizar PDFs", "📄 Markdown para PDF"], label_visibility="collapsed")
    st.divider()

# --- CONTENT ---
st.markdown('<p class="main-title">A Inteligência em Documentos.</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Gestão e otimização para o futuro da IA.</p>', unsafe_allow_html=True)

if selected == "📦 Converter Documentos":
    with st.container(border=True):
        st.subheader("Extração")
        file = st.file_uploader("Upload", type=["pdf", "docx", "doc", "xlsx", "pptx", "html"], label_visibility="collapsed")
        if file:
            fb = file.getvalue()
            st.info(f"**{file.name}** ({format_size(len(fb))})")
            img_on = st.toggle("Imagens", value=True)
            col_b1, col_b2 = st.columns([2, 1])
            if col_b1.button("🚀 Iniciar", type="primary", use_container_width=True):
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as tmp:
                    tmp.write(fb); tp = tmp.name
                try:
                    res = show_progress(run_async(markdownify.from_file, st.session_state.stop_event, tp, embed_images=img_on), time.time())
                    if res:
                        st.success("Concluído!"); st.download_button("📥 Baixar .md", res["val"], file_name="doc.md")
                        with st.expander("👀 Preview", expanded=True): st.markdown(res["val"], unsafe_allow_html=True)
                finally:
                    if os.path.exists(tp): os.remove(tp)
            col_b2.button("❌ Cancelar", on_click=on_cancel, use_container_width=True)

elif selected == "⚡ Otimizar PDFs":
    with st.container(border=True):
        st.subheader("Otimização")
        file_o = st.file_uploader("PDF", type=["pdf"], key="opt_up", label_visibility="collapsed")
        if file_o:
            ob = file_o.getvalue() # Armazenamos os bytes original em 'ob' (obytes)
            size_mb = len(ob) / (1024 * 1024)
            if size_mb > 30:
                st.error(f"Arquivo de **{size_mb:.1f}MB** excede o limite estável de 30MB.")
            else:
                st.info(f"**{file_o.name}** ({format_size(len(ob))})")
                co1, co2 = st.columns(2)
                with co1: st_mode = st.selectbox("Estratégia", ["Simples", "Agressiva"])
                with co2:
                    q_val = st.slider("Qualidade", 10, 100, 85)
                    d_val = st.select_slider("Resol.", options=[72, 100, 150, 200, 300], value=150) if "Agres" in st_mode else 150
                col_b1, col_b2 = st.columns([2, 1])
                if col_b1.button("⚡ Otimizar", type="primary", use_container_width=True):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(ob); tp = tmp.name
                    try:
                        m = "simple" if "Simp" in st_mode else "raster"
                        res = show_progress(run_async(markdownify.optimize_pdf, st.session_state.stop_event, tp, method=m, quality=q_val, dpi=d_val), time.time())
                        if res and not res.get("c", False):
                            st.markdown(f"""<div class="metrics-grid">
                                <div class="pro-metric"><p style="font-size:0.7rem; color:#64748B; margin:0;">ORIGINAL</p><p class="pro-metric-val">{format_size(len(ob))}</p></div>
                                <div class="pro-metric"><p style="font-size:0.7rem; color:#64748B; margin:0;">OTIMIZADO</p><p class="pro-metric-val">{format_size(len(res['val']))}</p></div>
                                <div class="pro-metric"><p style="font-size:0.7rem; color:#64748B; margin:0;">ECONOMIA</p><p class="pro-metric-val" style="color:#10B981;">{res['red']:.1f}%</p></div>
                            </div>""", unsafe_allow_html=True)
                            st.download_button("📥 Download PDF", res["val"], file_name="otimizado.pdf")
                    finally:
                        if os.path.exists(tp): os.remove(tp)
                col_b2.button("❌ Cancelar", on_click=on_cancel, use_container_width=True)

elif selected == "📄 Markdown para PDF":
    with st.container(border=True):
        st.subheader("Renderização")
        file_m = st.file_uploader("Markdown", type=["md", "txt"], label_visibility="collapsed")
        if file_m:
            col_b1, col_b2 = st.columns([2, 1])
            if col_b1.button("📄 Gerar PDF", type="primary", use_container_width=True):
                try:
                    txt = file_m.getvalue().decode("utf-8")
                    res = show_progress(run_async(markdownify.to_pdf, st.session_state.stop_event, txt), time.time())
                    if res: st.success("Pronto!"); st.download_button("📥 Download .pdf", res["val"], file_name="doc.pdf")
                except Exception as e: st.error(f"Erro: {e}")
            col_b2.button("❌ Cancelar", on_click=on_cancel, use_container_width=True)

st.divider()
st.caption("© 2024 canivete suíço - 2.5v")
