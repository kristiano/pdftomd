import streamlit as st
import os
import tempfile
import time
from leitor_pdf import Markdownify
from core import format_size

# Configuração da página com tema light forçado e layout wide
st.set_page_config(
    page_title="Canivete suíço para documentos | Pro", 
    page_icon="📄", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME LOGIC ---
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Sidebar Navigation & Theme Toggle
with st.sidebar:
    st.markdown('<p style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 1.5rem; font-weight: 800; margin-bottom: 0;">Master Ultra</p>', unsafe_allow_html=True)
    st.caption("v2.5 — Remodelador de docs")
    st.divider()
    
    # Theme Toggle
    st.session_state.dark_mode = st.toggle("🌙 Modo Escuro", value=st.session_state.dark_mode)
    st.divider()
    
    selected = st.radio(
        "Navegação Principal",
        ["📦 Converter Documentos", "⚡ Otimizar PDFs", "📄 Markdown para PDF"],
        index=0
    )
    
    st.divider()
    st.caption("Desenvolvido por Kristiano Plácido")

# Dynamic CSS based on Theme
if st.session_state.dark_mode:
    primary = "#818CF8"; primary_hover = "#6366F1"; bg_main = "#0F172A"; bg_card = "#1E293B"
    bg_sidebar = "#0B1120"; text_main = "#F8FAFC"; text_sub = "#94A3B8"; border = "#334155"; metric_bg = "#334155"
else:
    primary = "#4F46E5"; primary_hover = "#4338CA"; bg_main = "#FFFFFF"; bg_card = "#FFFFFF"
    bg_sidebar = "#F8FAFC"; text_main = "#0F172A"; text_sub = "#475569"; border = "#E2E8F0"; metric_bg = "#F8FAFC"

design_system_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {{ background-color: {bg_main} !important; }}
[data-testid="stHeader"] {{ background-color: transparent !important; }}

html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; color: {text_main} !important; }}
[data-testid="stSidebar"] {{ background-color: {bg_sidebar} !important; border-right: 1px solid {border} !important; }}

.main-title {{ font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 2.5rem; color: {text_main}; letter-spacing: -0.04em; }}
.sub-title {{ color: {text_sub}; font-size: 1.1rem; margin-bottom: 2rem; }}

[data-testid="stVerticalBlockBorderWrapper"] {{
    border: 1px solid {border} !important; border-radius: 16px !important;
    padding: 2rem !important; background-color: {bg_card} !important;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1) !important;
}}

.metrics-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 1.5rem 0; }}
.pro-metric {{ padding: 1.25rem; background: {metric_bg}; border: 1px solid {border}; border-radius: 12px; text-align: center; }}
.pro-metric-val {{ font-size: 1.5rem; font-weight: 700; color: {primary}; }}
.pro-metric-label {{ font-size: 0.75rem; font-weight: 600; color: {text_sub}; text-transform: uppercase; }}

div.stButton > button {{ background-color: {primary} !important; color: white !important; border-radius: 10px !important; padding: 0.75rem 1.5rem !important; font-weight: 600 !important; border: none !important; transition: all 0.2s ease-in-out !important; }}
div.stButton > button:hover {{ background-color: {primary_hover} !important; transform: translateY(-1px) !important; }}
div[data-testid="stDownloadButton"] > button {{ background-color: #10B981 !important; }}

hr {{ border-color: {border} !important; }}
[data-testid="stFileUploadDropzone"] {{ background: {bg_card} !important; border-color: {border} !important; }}
.stExpander {{ background-color: {bg_card} !important; border: 1px solid {border} !important; }}
</style>
"""
st.markdown(design_system_css, unsafe_allow_html=True)

# App Logic initialization
markdownify = Markdownify()

# --- MAIN PAGE HEADER ---
col_header_1, col_header_2 = st.columns([2, 1])
with col_header_1:
    st.markdown('<p class="main-title">A Inteligência em Documentos.</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-title" style="color: {text_sub};">Converta, otimize e estruture arquivos para o futuro da IA.</p>', unsafe_allow_html=True)

# --- WORKSPACE AREA ---
if selected == "📦 Converter Documentos":
    with st.container(border=True):
        st.subheader("Extração Universal para Markdown")
        st.write("Suporta PDF, DOCX, XLSX, PPTX e HTML. Otimizado para alta fidelidade e leitura por LLMs.")
        
        file = st.file_uploader("Arraste seu arquivo aqui", type=["pdf", "docx", "doc", "xlsx", "pptx", "html"], key="uploader_conv")
        
        if file:
            c1, c2 = st.columns([3, 1])
            with c1: st.info(f"**{file.name}** pronto para processamento. ({format_size(len(file.getvalue()))})")
            with c2: mode = st.toggle("Incluir Imagens", value=True, help="Embutir imagens em base64 no Markdown.")
            
            if st.button("🚀 Iniciar Conversão Inteligente", use_container_width=True):
                # MOVER PROGRESSUI PARA ANTES DE QUALQUER CARGA PESADA
                p_bar_conv = st.progress(0, "Preparando ambiente para extração...")
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as tmp:
                    tmp.write(file.getvalue()); tmp_path = tmp.name
                try:
                    p_bar_conv.progress(30, "Lendo e transformando documento...")
                    md = markdownify.from_file(tmp_path, embed_images=mode)
                    p_bar_conv.progress(100, "Concluído!")
                    time.sleep(1)
                    p_bar_conv.empty()
                    
                    st.success("Markdown gerado com sucesso.")
                    st.download_button("📥 Baixar Arquivo .md", md, file_name=f"{os.path.splitext(file.name)[0]}.md")
                    with st.expander("👀 Preview do Documento"): st.markdown(md, unsafe_allow_html=True)
                except Exception as e: 
                    p_bar_conv.empty()
                    st.error(f"Erro na extração: {e}")
                finally:
                    if os.path.exists(tmp_path): os.remove(tmp_path)

elif selected == "⚡ Otimizar PDFs":
    with st.container(border=True):
        st.subheader("Otimização Estrutural & Raster")
        st.write("Reduza o tamanho de PDFs acima de 50MB escolhendo uma estratégia. Arquivos grandes exigem mais memória.")
        
        file_opt = st.file_uploader("Selecione o PDF para otimizar", type=["pdf"], key="uploader_opt")
        
        if file_opt:
            orig_bytes = file_opt.getvalue()
            st.info(f"PDF carregado: **{file_opt.name}** ({format_size(len(orig_bytes))})")
            
            col_opt_1, col_opt_2 = st.columns(2)
            with col_opt_1: strat = st.selectbox("Estratégia", ["Simples (Preservar Texto)", "Agressiva (Converter para Imagem)"])
            with col_opt_1: 
                if len(orig_bytes) > 50*1024*1024:
                    st.warning("⚠️ Arquivo grande detectado. O processamento 'Agressivo' pode levar algum tempo.")
            with col_opt_2:
                qual = st.slider("Qualidade Visual", 10, 100, 85)
                dpi = st.select_slider("Resolução (DPI)", options=[72, 100, 150, 200, 300], value=150) if "Agressiva" in strat else 150
            
            if st.button("⚡ Executar Otimização"):
                # MOVER PROGRESS BAR PARA O TOPO ABSOLUTO DO CLICK
                progress_ui = st.progress(0, "Aguarde... Iniciando carregamento do arquivo em alta performance.")
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    # Divisão de tarefas para feedback imediato
                    progress_ui.progress(5, "Alocando arquivo temporário para processamento...")
                    tmp.write(orig_bytes); tmp_path = tmp.name
                
                try:
                    m_code = "simple" if "Simples" in strat else "raster"
                    progress_ui.progress(10, "Motor PyMuPDF inicializado. Iniciando otimização...")
                    
                    def ui_callback(p, t): 
                        # Escalar o progresso de 10% a 95% para o motor
                        final_p = 0.1 + (p * 0.85)
                        progress_ui.progress(final_p, text=t)
                    
                    compressed, reduction = markdownify.optimize_pdf(tmp_path, method=m_code, quality=qual, dpi=dpi, progress_callback=ui_callback)
                    
                    progress_ui.progress(100, text="Processamento finalizado!")
                    time.sleep(1)
                    progress_ui.empty()
                    
                    # Dashboard de Resultado Pro
                    st.markdown(f"""
                    <div class="metrics-grid">
                        <div class="pro-metric" style="background: {metric_bg}; border-color: {border};">
                            <p class="pro-metric-label">Original</p>
                            <p class="pro-metric-val">{format_size(len(orig_bytes))}</p>
                        </div>
                        <div class="pro-metric" style="background: {metric_bg}; border-color: {border};">
                            <p class="pro-metric-label">Otimizado</p>
                            <p class="pro-metric-val">{format_size(len(compressed))}</p>
                        </div>
                        <div class="pro-metric" style="background: {metric_bg}; border-color: {border};">
                            <p class="pro-metric-label">Economia</p>
                            <p class="pro-metric-val" style="color: #10B981;">{reduction:.1f}%</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.download_button("📥 Baixar PDF Otimizado", compressed, file_name=f"{os.path.splitext(file_opt.name)[0]}_opt.pdf")
                except Exception as e: 
                    progress_ui.empty()
                    st.error(f"Erro: {e}")
                finally:
                    if os.path.exists(tmp_path): os.remove(tmp_path)

elif selected == "📄 Markdown para PDF":
    with st.container(border=True):
        st.subheader("Renderizador Profissional WeasyPrint")
        st.write("Converta documentos Markdown em PDFs elegantes.")
        
        file_md = st.file_uploader("Upload do arquivo .md", type=["md", "markdown", "txt"], key="uploader_md")
        
        if file_md:
            if st.button("📄 Gerar PDF Master"):
                try:
                    text = file_md.getvalue().decode("utf-8")
                    with st.spinner("Desenhando PDF com CSS GitHub..."): pdf = markdownify.to_pdf(text)
                    st.success("Renderização concluída.")
                    st.download_button("📥 Baixar PDF Renderizado", pdf, file_name=f"documento_renderizado.pdf")
                except Exception as e: st.error(f"Erro: {e}")

# --- FOOTEER ---
st.divider()
f_col1, f_col2 = st.columns([3, 1])
with f_col2: st.caption("© 2024 canivete suíço para documentos — Kristiano Plácido")
