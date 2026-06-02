import streamlit as st

from services.pdf_service import process_pdf
from services.rag_service import (
    setup_rag,
    ask_question
)

from services.company_tool import company_tool

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

# ================= PDF =================

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

# ================= PROCESS PDF =================

if uploaded_file:

    pdf_path = f"data/uploaded_pdfs/{uploaded_file.name}"

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("PDF Uploaded ✅")

    with st.spinner("Processing PDF..."):

        chunks = process_pdf(pdf_path)

    st.success(f"{len(chunks)} chunks created ✅")

    with st.spinner("Setting up RAG..."):

        retriever = setup_rag(chunks)

    st.session_state.retriever = retriever

    st.success("RAG Ready ✅")

# ================= QUESTION =================

question = st.text_input("Ask a question")

if question:

    # ================= TOOL CHECK =================

    tool_answer = company_tool(question)

    if tool_answer:

        st.session_state.chat_history.append({

            "question": question,
            "answer": tool_answer,
            "docs": []

        })

    else:

        # ================= RAG =================

        if st.session_state.retriever is not None:

            answer, docs = ask_question(
                question,
                st.session_state.retriever
            )

            st.session_state.chat_history.append({

                "question": question,
                "answer": answer,
                "docs": docs

            })

        else:

            st.session_state.chat_history.append({

                "question": question,
                "answer": "Please upload a PDF first.",
                "docs": []

            })

# ================= DISPLAY =================

for chat in st.session_state.chat_history:

    st.subheader("Question")
    st.write(chat["question"])

    st.subheader("Answer")
    st.write(chat["answer"])

    if chat["docs"]:

        st.subheader("Sources")

        pages = set()

        for d in chat["docs"]:

            page = d.metadata.get("page", "?")

            if page not in pages:

                pages.add(page)

                st.write(f"📌 Page {page}")

    st.divider()