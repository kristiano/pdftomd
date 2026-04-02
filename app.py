import streamlit as st
import os
import tempfile
from leitor_pdf import converter_pdf_para_md

st.set_page_config(page_title="PDF para Markdown", page_icon="📄")

st.title("Conversor de PDF para Markdown")
st.write("Faça o upload de um arquivo PDF e converta para formato Markdown (.md).")

uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf")

if uploaded_file is not None:
    # Cria os recursos visuais de aguarde
    with st.spinner("Processando o arquivo PDF, por favor aguarde..."):
        # Salva o arquivo temporariamente pois a função leitor_pdf espera um caminho de arquivo
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            # Chama a função existente que converte o PDF
            md_file_path = converter_pdf_para_md(tmp_file_path)
            
            # Lê o conteúdo do arquivo gerado para disponibilizar para download
            with open(md_file_path, "r", encoding="utf-8") as f:
                md_content = f.read()
                
            st.success("Conversão concluída com sucesso!")
            
            # Botão de download
            novo_nome_arquivo = uploaded_file.name.replace(".pdf", ".md")
            st.download_button(
                label="📥 Baixar Arquivo Markdown",
                data=md_content,
                file_name=novo_nome_arquivo,
                mime="text/markdown"
            )
            
            # Exibe uma preview do markdown na tela (opcional, até certo tamanho)
            with st.expander("Pré-visualizar o conteúdo"):
                st.markdown(md_content)
            
        except Exception as e:
            st.error(f"Ocorreu um erro durante a conversão: {e}")
            
        finally:
            # Limpa os arquivos temporários criados
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)
            if 'md_file_path' in locals() and os.path.exists(md_file_path):
                os.remove(md_file_path)
