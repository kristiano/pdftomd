import streamlit as st
import os
import tempfile
import time
from leitor_pdf import converter_pdf_para_md

st.set_page_config(page_title="PDF para Markdown", page_icon="📄", layout="centered")

st.title("📄 Conversor de PDF para Markdown")
st.markdown("Transforme seus documentos PDF em texto formatado `.md` com visualização prévia e download simplificado.")

st.divider()

# Centraliza e melhora o visual do uploader
uploaded_file = st.file_uploader("Arraste e solte ou clique para escolher um arquivo PDF", type="pdf")

if uploaded_file is not None:
    # Verificação de segurança adicional para o formato do arquivo
    if not uploaded_file.name.lower().endswith('.pdf'):
        st.error("⚠️ **Atenção:** Formato de arquivo não suportado! O aplicativo aceita apenas arquivos com a extensão **.pdf**.")
        st.stop()

    st.info(f"Arquivo selecionado: **{uploaded_file.name}**")
    
    # Adicionando botão que dispara a conversão para dar controle ao usuário
    if st.button("🚀 Converter para .md", use_container_width=True, type="primary"):
        
        # Criação da barra de progresso visual
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("Preparando o ambiente e validando arquivo...")
        progress_bar.progress(10)
        time.sleep(0.3)
        
        # Salva o arquivo temporariamente
        status_text.text("Carregando páginas do arquivo...")
        progress_bar.progress(30)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        time.sleep(0.3)
        status_text.text("Processando leitura com biblioteca PyMuPDF4LLM... (Isso pode levar alguns segundos)")
        progress_bar.progress(50)

        try:
            # Chama a função principal de conversão
            md_file_path = converter_pdf_para_md(tmp_file_path)
            
            progress_bar.progress(80)
            status_text.text("Organizando o documento em Markdown...")
            
            # Lê o conteúdo do arquivo Markdown gerado
            with open(md_file_path, "r", encoding="utf-8") as f:
                md_content = f.read()
                
            progress_bar.progress(100)
            status_text.text("Pronto!")
            time.sleep(0.5)
            
            # Limpa textos e barra pra não poluir a interface depois de baixar
            progress_bar.empty()
            status_text.empty()
            
            st.success("✅ Conversão concluída com sucesso!")
            
            novo_nome_arquivo = uploaded_file.name.replace(".pdf", ".md")
            
            # Botão de download visualmente destacado
            st.download_button(
                label="📥 Baixar Arquivo Markdown",
                data=md_content,
                file_name=novo_nome_arquivo,
                mime="text/markdown",
                use_container_width=True
            )
            
            st.divider()
            
            # Exibe uma preview do markdown na tela dentro de um container com rolagem (simulado com expander)
            with st.expander("👀 Cique aqui para pré-visualizar o conteúdo (Preview)"):
                st.markdown(md_content)
            
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Ocorreu um erro durante a conversão: {e}")
            
        finally:
            # Serviço de limpeza dos temporários nos bastidores
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)
            if 'md_file_path' in locals() and os.path.exists(md_file_path):
                os.remove(md_file_path)
