# Conversor de PDF para Markdown

Aplicativo web funcional construído em [Streamlit](https://streamlit.io/) para a leitura de arquivos PDF e conversão automática do seu texto em formato Markdown (`.md`).
Ele utiliza a biblioteca subjacente `pymupdf4llm` para realizar uma extração de texto em alta fidelidade voltada para documentação em geral ou para uso direto em modelos de linguagem (LLMs).

## 🚀 Como funciona

Acesse a interface, clique em **Browse files** e faça o upload de um documento PDF. O sistema salva o arquivo localmente de maneira temporária, aciona o script subjacente para efetuar a leitura com `pymupdf` e disponibiliza para o usuário um botão para baixar o retorno `.md`.

## ⚙️ Instalação

Pré-requisito: Python 3 instalado na sua máquina.

1. Clone esse repositório:
```bash
git clone https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git
cd "NOME-DO-REPOSITORIO"
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
- Mac/Linux:
```bash
source venv/bin/activate
```
- Windows:
```bash
venv\Scripts\activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## ▶️ Executando a Aplicação

Inicie o servidor do Streamlit:
```bash
streamlit run app.py
```
O navegador abrirá automaticamente em `http://localhost:8501`.
