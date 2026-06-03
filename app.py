import streamlit as st
from dotenv import load_dotenv

from services.pdf_service import process_pdf
from services.rag_service import setup_rag, ask_question

from services.company_tool import company_tool
from services.web_search_tool import tavily_search

from services.calculator_tool import calculator_tool
from services.date_tool import date_tool

# ================= LOAD ENV =================

load_dotenv()

# ================= PAGE =================

st.set_page_config(
    page_title="Multimodal RAG Bot",
    layout="wide"
)

st.title("📚 Multimodal RAG Bot (Multi Tool + RAG)")

# ================= SESSION =================

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

# ================= PDF UPLOAD =================

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    if st.session_state.uploaded_file_name != uploaded_file.name:

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
        st.session_state.uploaded_file_name = uploaded_file.name

        st.success("RAG Ready ✅")

# ================= QUESTION =================

question = st.text_input("Ask a question")

if question and len(question.strip()) >= 2:

    answer = None
    docs = []
    source = ""

    # ================= 1 DATABASE TOOL =================

    db_result = company_tool(question)

    if db_result:

        answer = db_result
        source = "database"

    else:

        # ================= 2 CALCULATOR TOOL =================

        calc_result = calculator_tool(question)

        if calc_result:

            answer = calc_result
            source = "calculator"

        else:

            # ================= 3 DATE TOOL =================

            date_result = date_tool(question)

            if date_result:

                answer = date_result
                source = "date"

            else:

                # ================= PDF RELATED QUESTIONS =================

                pdf_keywords = [
                    "pdf",
                    "document",
                    "uploaded file",
                    "this file",
                    "this document",
                    "this pdf",
                    "summarize",
                    "summary"
                ]

                is_pdf_question = any(
                    word in question.lower()
                    for word in pdf_keywords
                )

                # ================= 4 PDF RAG =================

                if is_pdf_question:

                    if st.session_state.retriever is not None:

                        answer, docs = ask_question(
                            question,
                            st.session_state.retriever
                        )

                        source = "pdf_rag"

                    else:

                        answer = "Please upload a PDF first."
                        source = "none"

                else:

                    # ================= 5 WEB SEARCH =================

                    web_result = tavily_search(question)

                    if web_result:

                        answer = web_result
                        source = "web"

                    else:

                        # ================= FALLBACK TO RAG =================

                        if st.session_state.retriever is not None:

                            answer, docs = ask_question(
                                question,
                                st.session_state.retriever
                            )

                            source = "pdf_rag"

                        else:

                            answer = "No information found."
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

    st.caption(f"Source : {chat['source']}")

    if chat["docs"]:

        st.subheader("Sources")

        pages = set()

        for d in chat["docs"]:

            page = d.metadata.get("page", "?")

            if page not in pages:

                pages.add(page)

                st.write(f"📌 Page {page}")

    st.divider()