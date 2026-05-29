# Multimodal RAG Bot

A modular Multimodal Retrieval-Augmented Generation (RAG) chatbot built using Streamlit, LangChain, FAISS, and Groq LLM.

---

# Features

- PDF Question Answering
- OCR Support for Scanned PDFs
- Table & Graph Understanding
- FAISS Semantic Retrieval
- Groq LLM Integration
- Multi-question Chat Support
- Source-aware Answers
- Modular Architecture

---

# Tech Stack

- Python
- Streamlit
- LangChain
- FAISS
- Groq API
- Tesseract OCR
- Poppler

---

# Project Structure

```text
multimodal-rag-bot/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── core/
│   ├── loader.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── retriever.py
│   └── generation.py
│
├── services/
│   ├── pdf_service.py
│   └── rag_service.py
│
├── data/
│   └── uploaded_pdfs/
│
├── vectorstore/
│
├── utils/
│
└── assets/
    └── rag-architecture.png
```

---

# System Design

![RAG Architecture](assets/rag-architecture.png)

---

# Workflow

1. User uploads PDF
2. PDF text extraction happens
3. Text is split into chunks
4. Embeddings are generated
5. FAISS vectorstore stores embeddings
6. User asks question
7. Retriever fetches relevant chunks
8. Groq LLM generates final answer

---

# Modular Architecture

- `core/` → Core RAG pipeline
- `services/` → Business logic layer
- `data/` → Uploaded PDFs
- `vectorstore/` → FAISS index
- `utils/` → Helper functions

---

# Run Locally

## Clone Repository

```bash
git clone https://github.com/ChikkalaSukrutiNaidu/multimodal-rag-bot.git
```

## Install Requirements

```bash
pip install -r requirements.txt
```

## Run Streamlit App

```bash
streamlit run app.py
```

---

# Future Enhancements

- Hybrid Search
- Reranking
- Image Retrieval
- Multi-PDF Chat
- ChromaDB / Pinecone Support
- Deployment on HuggingFace / Render

---

