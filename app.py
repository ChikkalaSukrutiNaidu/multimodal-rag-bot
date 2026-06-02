import streamlit as st
import os
from dotenv import load_dotenv

from services.pdf_service import process_pdf
from services.rag_service import setup_rag, ask_question
from services.company_tool import company_tool
from services.web_search_tool import tavily_search   # NEW

# ================= LOAD ENV =================
load_dotenv()

# ================= PAGE =================
st.set_page_config(
    page_title="Multimodal RAG Bot",
    layout="wide"
)

st.title("📚 Multimodal RAG Bot (Tool + RAG + Web)")

# ================= SESSION =================
if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ================= PDF UPLOAD =================
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

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

    answer = None
    docs = []

    # ================= 1. DATABASE TOOL =================
    tool_answer = company_tool(question)

    if tool_answer:
        answer = tool_answer
        source = "database"

    else:

        # ================= 2. TAVILY WEB SEARCH =================
        web_result = tavily_search(question)

        if web_result:
            answer = web_result
            source = "web"

        else:

            # ================= 3. RAG =================
            if st.session_state.retriever is not None:
                answer, docs = ask_question(
                    question,
                    st.session_state.retriever
                )
                source = "pdf_rag"

            else:
                answer = "Please upload a PDF first."
                source = "none"

    # ================= SAVE CHAT =================
    st.session_state.chat_history.append({
        "question": question,
        "answer": answer,
        "docs": docs,
        "source": source
    })

# ================= DISPLAY =================
for chat in st.session_state.chat_history:

    st.subheader("Question")
    st.write(chat["question"])

    st.subheader("Answer")
    st.write(chat["answer"])

    st.caption(f"Source: {chat['source']}")

    if chat["docs"]:

        st.subheader("Sources")

        pages = set()

        for d in chat["docs"]:
            page = d.metadata.get("page", "?")
            if page not in pages:
                pages.add(page)
                st.write(f"📌 Page {page}")

    st.divider()