# 📄 Canivete Suíço para Documentos — v2.8 (Expert)

O **Canivete Suíço Master** é uma aplicação Streamlit de alta performance projetada para converter, extrair e renderizar documentos com precisão industrial e velocidade extrema. Inspirado nos melhores servidores MCP (*Model Context Protocol*), este projeto utiliza uma arquitetura assíncrona para garantir uma experiência de usuário fluida e sem travamentos.

---

## 🚀 Funcionalidades Principais

### 📦 1. Conversor Universal para Markdown
Extraia conteúdo de quase qualquer formato para Markdown limpo, ideal para uso em LLMs (ChatGPT, Claude, etc.).
- **PDF Inteligente**: Utiliza `pymupdf4llm` para extrair texto, tabelas e preservar a estrutura original.
- **Office & Docs**: Suporte nativo para Word (.docx), Excel (.xlsx), PowerPoint (.pptx) e HTML via motor **MarkItDown** (Microsoft).
- **Gestão de Imagens**: Opção para embutir imagens diretamente no Markdown via Base64 ou remover ruídos visuais.

### 📄 2. Renderizador Master (Markdown para PDF)
Transforme textos Markdown em documentos PDF profissionais com velocidade 20x superior à média.
- **Motor FPDF2**: Substitui motores lentos (como WeasyPrint) por um sistema de renderização nativa de alta performance.
- **Design ECharts**: Estética baseada em Slate/Indigo, com suporte a alertas GFM (Nota, Dica, Importante, Aviso).
- **Tipografia Moderna**: Renderização limpa de cabeçalhos, listas e imagens embutidas.

---

## 🛠️ Diferenciais Técnicos (Arquitetura Expert)

- **Concorrência Assíncrona**: Todas as tarefas pesadas rodam em *Background Threads* com filas de comunicação (`queue`), permitindo que múltiplos usuários utilizem o app sem bloqueios.
- **Telemetria em Tempo Real**: Barra de progresso granular com cálculo de porcentagem (%) e **ETA (Tempo Estimado)** dinâmico.
- **Interrupção Prioritária**: Botão "Cancelar" em todas as ferramentas que utiliza sinalização de thread para interromper processos instantaneamente, economizando recursos do servidor.
- **UI/UX Premium**: Design baseado em HSL personalizado, modo clean com sidebar persistente e componentes responsivos.

---

## 💻 Instalação e Uso

### Dependências Core
```bash
pip install streamlit pymupdf pymupdf4llm markitdown fpdf2 Pillow markdown
```

### Rodando Localmente
```bash
streamlit run app.py
```

---

## 🏗️ Estrutura do Projeto

```text
├── app.py                # Interface Streamlit e Gestão de Threads
├── leitor_pdf.py         # Fachada (Orquestrador) do Sistema
├── core/
│   ├── extractor.py      # Lógica de conversão PDF/Office -> MD
│   ├── pdf_generator.py  # Renderizador Ultra-rápido (FPDF2)
│   ├── compressor.py     # Motor de Otimização (Opcional/Interno)
│   └── styles.py         # Tokens de Design e Temas
└── requirements.txt      # Dependências do Projeto
```

---

## ⚖️ Licença e Créditos
Desenvolvido por **Kristiano Plácido** — Focado em ferramentas de produtividade para a era da inteligência artificial.

> [!TIP]
> Para documentos extremamente longos, utilize o modo de conversão sem imagens para acelerar ainda mais o tempo de processamento.
