import streamlit as st
import os
import tempfile
import time
from leitor_pdf import Markdownify

st.set_page_config(page_title="Markdownify Universal", page_icon="📄", layout="centered")

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
