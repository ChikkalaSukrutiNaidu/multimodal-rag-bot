# Multimodal RAG Bot

A modular Multimodal Retrieval-Augmented Generation (RAG) chatbot built using Streamlit, LangChain, FAISS, and Groq LLM.

## Features

- PDF Question Answering
- OCR support for scanned PDFs
- FAISS semantic retrieval
- Groq LLM integration
- Modular architecture
- Multi-question chat support
- Source-aware answers

## Tech Stack

- Python
- Streamlit
- LangChain
- FAISS
- Groq API
- Tesseract OCR
- Poppler

## Project Structure

```text
core/       -> RAG pipeline logic
services/   -> orchestration layer
data/       -> uploaded PDFs
app.py      -> Streamlit frontend