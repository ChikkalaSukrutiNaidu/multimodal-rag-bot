import streamlit as st

from utils.pdf_loader import load_pdf
from utils.chunking import split_documents
from utils.embeddings import create_vectorstore
from utils.retriever import get_retriever
from utils.generation import generate_answer

# ================= PAGE =================

st.set_page_config(
    page_title="Multimodal RAG Bot",
    layout="wide"
)

st.title("📚 Multimodal RAG Bot")

# ================= SESSION =================

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

# ================= FILE UPLOAD =================

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

# ================= PROCESS PDF =================

if uploaded_file and not st.session_state.pdf_processed:

    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("PDF Uploaded ✅")

    # LOAD PDF

    with st.spinner("Loading PDF..."):

        documents = load_pdf(uploaded_file.name)

    st.success("PDF Loaded ✅")

    # CHUNKING

    with st.spinner("Creating Chunks..."):

        chunks = split_documents(documents)

    st.success(f"{len(chunks)} chunks created ✅")

    # VECTORSTORE

    with st.spinner("Creating Vectorstore..."):

        vectorstore = create_vectorstore(chunks)

    retriever = get_retriever(vectorstore)

    st.session_state.retriever = retriever
    st.session_state.pdf_processed = True

    st.success("FAISS Vectorstore Ready ✅")

# ================= QUESTIONS =================

if st.session_state.retriever is not None:

    question = st.text_input("Ask a question")

    if st.button("Submit Question"):

        if question.strip():

            with st.spinner("Generating Answer..."):

                answer, docs = generate_answer(
                    question,
                    st.session_state.retriever
                )

            st.session_state.chat_history.append({

                "question": question,
                "answer": answer,
                "docs": docs

            })

# ================= CHAT DISPLAY =================

for chat in reversed(st.session_state.chat_history):

    st.subheader("Question")
    st.write(chat["question"])

    st.subheader("Answer")
    st.write(chat["answer"])

    st.subheader("Sources")

    shown_pages = set()

    for d in chat["docs"]:

        page = d.metadata.get("page", "?")

        if page not in shown_pages:

            shown_pages.add(page)

            st.write(f"📌 Page {page}")

    st.divider()