import streamlit as st

from utils.docling_loader import load_pdf
from utils.chunking import split_documents
from utils.embeddings import create_vectorstore
from utils.retriever import get_retriever
from utils.generation import generate_answer


# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="Multimodal RAG Bot",
    layout="wide"
)

st.title("📚 Multimodal RAG Bot")
st.write("Upload a PDF and ask questions.")


# ================= PDF UPLOAD =================

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)


# ================= MAIN PIPELINE =================

if uploaded_file is not None:

    # SAVE FILE
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"Uploaded: {uploaded_file.name}")

    # ================= LOAD PDF =================

    with st.spinner("Loading PDF..."):

        documents = load_pdf(uploaded_file.name)

    st.success("PDF Loaded Successfully ✅")

    st.write(f"Loaded {len(documents)} pages")

    # ================= CHUNKING =================

    with st.spinner("Splitting document..."):

        chunks = split_documents(documents)

    st.success(f"Created {len(chunks)} chunks ✅")

    # ================= VECTOR STORE =================

    with st.spinner("Creating FAISS vectorstore..."):

        vectorstore = create_vectorstore(chunks)

    st.success("FAISS Vectorstore Ready ✅")

    # ================= RETRIEVER =================

    retriever = get_retriever(vectorstore)

    # ================= QUESTION =================

    question = st.text_input("Ask a question")

    if question:

        with st.spinner("Generating Answer..."):

            answer, docs = generate_answer(
                question,
                retriever
            )

        # ================= ANSWER =================

        st.subheader("Answer")

        st.write(answer)

        # ================= SOURCES =================

        st.subheader("Sources")

        if docs:

            for d in docs:

                source = d.metadata.get(
                    "source",
                    "Unknown"
                )

                page = d.metadata.get(
                    "page",
                    "?"
                )

                st.write(f"📌 {source} - Page {page}")

        else:

            st.write("No sources found.")