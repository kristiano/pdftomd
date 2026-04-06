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

.metrics-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin: 2rem 0; }
.pro-metric { padding: 1.5rem; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; text-align: center; }
.pro-metric-val { font-size: 1.8rem; font-weight: 800; color: #4F46E5; }

div.stButton > button {
    background-color: #4F46E5 !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 0.7rem 1.5rem !important;
    font-weight: 600 !important;
    width: 100%;
    border: none;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    background-color: #4338CA !important;
    transform: translateY(-1px);
}

div.cancel-btn-container button {
    background-color: #FEE2E2 !important;
    color: #EF4444 !important;
    border: 1px solid #FCA5A5 !important;
}
div.cancel-btn-container button:hover {
    background-color: #EF4444 !important;
    color: white !important;
}

div[data-testid="stDownloadButton"] > button { background-color: #10B981 !important; border: none; }
</style>
"""
st.markdown(design_system_css, unsafe_allow_html=True)

markdownify = st.session_state.engine

# Helper para monitorar threads e progresso unificado com cálculos de tempo
def run_in_thread(engine_method, *args, **kwargs):
    q = queue.Queue()
    def wrapper():
        try:
            # Injetar o callback de progresso para a thread capturar (%) e status
            def cb(p, t): 
                q.put({"type": "p", "v": p, "t": t})
                return False
            kwargs["progress_callback"] = cb
            
            res = engine_method(*args, **kwargs)
            if isinstance(res, tuple):
                q.put({"type": "r", "val": res[0], "red": res[1], "c": res[2]})
            else:
                q.put({"type": "r", "val": res})
        except Exception as e:
            q.put({"type": "e", "m": str(e)})
    
    t = threading.Thread(target=wrapper)
    t.start()
    return q

def monitor_progress(q, prog_ui, start_time):
    """Loop unificado de monitoramento de progresso com cálculo de ETA para todas ferramentas."""
    finished = False
    result = None
    while not finished:
        try:
            msg = q.get(timeout=0.1)
            if msg["type"] == "p":
                # TELEMETRIA: Cálculo de ETA unificado (Estimated Time for Arrival)
                elapsed = time.time() - start_time
                progress_val = msg["v"]
                if progress_val > 0.05:
                    total_estimado = elapsed / progress_val
                    restante = int(total_estimado - elapsed)
                    eta_text = f"| ETA: ~{restante}s restantes" if restante > 0 else "| Finalizando..."
                else:
                    eta_text = "| Calculando tempo..."
                
                # Exibir Porcentagem EM NEGRITO + Texto + ETA
                perc_str = f"**{int(progress_val*100)}%**"
                prog_ui.progress(progress_val, text=f"{perc_str} • {msg['t']} {eta_text}")
            elif msg["type"] == "r":
                prog_ui.empty()
                result = msg
                finished = True
            elif msg["type"] == "e":
                prog_ui.empty()
                st.error(f"Erro no processamento: {msg['m']}")
                finished = True
        except queue.Empty:
            # Liberar o processador para outras sessões Streamlit (GIL Yielding)
            time.sleep(0.05)
    return result

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 25px;">
            <div style="background-color: #4F46E5; width: 42px; height: 42px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 12px;">
                <span style="color: white; font-size: 22px; font-weight: bold;">C</span>
            </div>
            <div><h2 style="margin: 0; font-size: 1.25rem; font-weight: 800; color: #0F172A;">Canivete Suíço</h2><p style="margin: 0; font-size: 0.75rem; color: #64748B;">v2.5 — Docs Pro</p></div>
        </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("### 🛠️ Ferramentas")
    selected = st.selectbox("Operação", ["📦 Converter Documentos", "⚡ Otimizar PDFs", "📄 Markdown para PDF"], index=0, label_visibility="collapsed")
    st.divider()
    st.markdown("""
        <div style="padding: 12px; border-radius: 10px; background-color: #FFFFFF; border: 1px solid #E2E8F0;">
            <p style="margin: 0; font-size: 0.7rem; color: #64748B; font-weight: 600;">Desenvolvido por</p>
            <p style="margin: 0; font-size: 0.9rem; font-weight: 700; color: #0F172A;">Kristiano Plácido</p>
        </div>
    """, unsafe_allow_html=True)

# --- MAIN CONTENT ---
st.markdown('<p class="main-title">A Inteligência em Documentos.</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Monitoramento completo de progresso e tempo estimado em tempo real.</p>', unsafe_allow_html=True)

if selected == "📦 Converter Documentos":
    with st.container(border=True):
        st.subheader("Extração Universal para Markdown")
        file = st.file_uploader("Upload do documento", type=["pdf", "docx", "doc", "xlsx", "pptx", "html"], label_visibility="collapsed")
        if file:
            c1, c2 = st.columns([3, 1])
            with c1: st.info(f"**{file.name}** ({format_size(len(file.getvalue()))})")
            with c2: mode = st.toggle("Incluir Imagens", value=True)
            
            c_bt1, c_bt2 = st.columns(2)
            prog_area = st.empty()
            with c_bt2:
                st.markdown('<div class="cancel-btn-container">', unsafe_allow_html=True)
                if st.button("❌ Cancelar Conversão"): st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with c_bt1:
                if st.button("🚀 Iniciar Conversão Inteligente", type="primary"):
                    start = time.time()
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as tmp:
                        tmp.write(file.getvalue()); tp = tmp.name
                    try:
                        p_ui = prog_area.progress(0, "Aguarde...")
                        q = run_in_thread(markdownify.from_file, tp, embed_images=mode)
                        res = monitor_progress(q, p_ui, start)
                        if res and "val" in res:
                            st.success("Extração completa!"); st.download_button("📥 Baixar .md", res["val"], file_name=f"{os.path.splitext(file.name)[0]}.md")
                    finally:
                        if os.path.exists(tp): os.remove(tp)

elif selected == "⚡ Otimizar PDFs":
    with st.container(border=True):
        st.subheader("Otimização Inteligente de PDFs")
        file_opt = st.file_uploader("Upload", type=["pdf"], key="uploader_opt", label_visibility="collapsed")
        if file_opt:
            orig_bytes = file_opt.getvalue()
            st.info(f"**{file_opt.name}** ({format_size(len(orig_bytes))})")
            c_opt1, c_opt2 = st.columns(2)
            with c_opt1: strat = st.selectbox("Estratégia", ["Simples (Preservar Texto)", "Agressiva (Rasterizar)"])
            with c_opt2:
                qual = st.slider("Qualidade", 10, 100, 85)
                dpi = st.select_slider("Resolução", options=[72, 100, 150, 200, 300], value=150) if "Agressiva" in strat else 150
            
            c_bt1, c_bt2 = st.columns(2)
            p_area = st.empty()
            with c_bt2:
                st.markdown('<div class="cancel-btn-container">', unsafe_allow_html=True)
                if st.button("❌ Cancelar Otimização"): st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with c_bt1:
                if st.button("⚡ Executar Otimização", type="primary"):
                    start = time.time()
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(orig_bytes); tp = tmp.name
                    try:
                        p_ui = p_area.progress(0, "Iniciando motor...")
                        m = "simple" if "Simples" in strat else "raster"
                        q = run_in_thread(markdownify.optimize_pdf, tp, method=m, quality=qual, dpi=dpi)
                        res = monitor_progress(q, p_ui, start)
                        if res and not res.get("c", False):
                            st.markdown(f"""<div class="metrics-grid">
                                <div class="pro-metric"><p style="font-size:0.75rem; color:#64748B; margin:0; text-transform:uppercase;">Original</p><p class="pro-metric-val">{format_size(len(orig_bytes))}</p></div>
                                <div class="pro-metric"><p style="font-size:0.75rem; color:#64748B; margin:0; text-transform:uppercase;">Reduzido</p><p class="pro-metric-val">{format_size(len(res['val']))}</p></div>
                                <div class="pro-metric"><p style="font-size:0.75rem; color:#64748B; margin:0; text-transform:uppercase;">Economia</p><p class="pro-metric-val" style="color:#10B981;">{res['red']:.1f}%</p></div>
                            </div>""", unsafe_allow_html=True)
                            st.download_button("📥 Baixar PDF Otimizado", res["val"], file_name=f"{os.path.splitext(file_opt.name)[0]}_opt.pdf")
                    finally:
                        if os.path.exists(tp): os.remove(tp)

elif selected == "📄 Markdown para PDF":
    with st.container(border=True):
        st.subheader("Renderizador WeasyPrint Master")
        file_md = st.file_uploader("Upload .md", type=["md", "markdown", "txt"], label_visibility="collapsed")
        if file_md:
            c_bt1, c_bt2 = st.columns(2)
            p_area = st.empty()
            with c_bt2:
                st.markdown('<div class="cancel-btn-container">', unsafe_allow_html=True)
                if st.button("❌ Cancelar Renderização"): st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with c_bt1:
                if st.button("📄 Gerar PDF Renderizado", type="primary"):
                    start = time.time()
                    try:
                        text = file_md.getvalue().decode("utf-8")
                        p_ui = p_area.progress(0, "Iniciando renderização...")
                        q = run_in_thread(markdownify.to_pdf, text)
                        res = monitor_progress(q, p_ui, start)
                        if res and "val" in res:
                            st.success("Renderização pronta!"); st.download_button("📥 Baixar PDF", res["val"], file_name="renderizado.pdf")
                    except Exception as e: st.error(f"Erro: {e}")

# Footer
st.divider()
st.caption("© 2024 canivete suíço para documentos — Kristiano Plácido")
