import streamlit as st
from dotenv import load_dotenv
from graph.workflow import graph

from services.pdf_service import process_pdf
from services.rag_service import setup_rag, ask_question

from services.company_tool import company_tool
from services.web_search_tool import tavily_search

from services.calculator_tool import calculator_tool
from services.date_tool import date_tool

from audio_recorder_streamlit import audio_recorder
from services.voice_tool import speech_to_text

from services.translation_tool import translate_to_english
from services.company_name_corrector import correct_company_names
def normalize_query(query):

    query = query.lower()

    mappings = {

        # PDF related
        "pidief": "pdf",
        "p d f": "pdf",
        "pee dee ef": "pdf",
        "uploaded pdf": "pdf",
        "uploaded document": "document",

        # Company names
        "టీసీఎస్": "tcs",
        "టి సి ఎస్": "tcs",
        "t c s": "tcs",

        "విప్రో": "wipro",
        "ఇన్ఫోసిస్": "infosys",

        # CEO
        "సీఈఓ": "ceo",
        "సిఈఓ": "ceo"
    }

    for k, v in mappings.items():
        query = query.replace(k.lower(), v)

    return query

    for k, v in mappings.items():
        query = query.replace(k.lower(), v)

    return query

# ================= LOAD ENV =================

load_dotenv()

# ================= PAGE =================

st.set_page_config(
    page_title="Multimodal RAG Bot",
    layout="wide"
)

st.title("📚 Multimodal RAG Bot (Voice + Multi Tool + RAG)")
st.markdown("""
<style>

.main {
    background-color: #F8FAFC;
}

h1 {
    color: #1E3A8A;
}

.stButton > button {
    background-color: #2563EB;
    color: white;
    border-radius: 10px;
}

.stTextInput > div > div > input {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ================= SESSION =================

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

if "last_question" not in st.session_state:
    st.session_state.last_question = ""

if "voice_query" not in st.session_state:
    st.session_state.voice_query = None

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

# ================= TEXT SEARCH =================

st.subheader("⌨️ Text Search")

text_question = st.text_input("Ask a question")

# ================= VOICE SEARCH =================

st.subheader("🎤 Voice Search")

voice_language = st.selectbox(
    "Select Voice Language",
    [
        "Auto Detect",
        "English",
        "Telugu",
        "Hindi"
    ]
)

lang_map = {
    "Auto Detect": None,
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi"
}

audio_bytes = audio_recorder(key="voice_recorder_main")

if audio_bytes:

    with st.spinner("Converting speech to text..."):

        voice_result = speech_to_text(
            audio_bytes,
            lang_map[voice_language]
        )

    voice_question = voice_result["text"]
    detected_language = voice_result["language"]

    st.success(
        f"Recognized ({detected_language}) : {voice_question}"
    )

    translated_text = translate_to_english(
        voice_question
    )

    translated_text = correct_company_names(
        translated_text
    )

    st.info(
        f"English Translation : {translated_text}"
    )

    if st.button("Use Voice Query", key="voice_query_btn"):
        st.session_state["use_voice"] = True

        st.session_state.voice_query = translated_text

audio_bytes = audio_recorder()

if audio_bytes:

    with st.spinner("Converting speech to text..."):

        voice_result = speech_to_text(audio_bytes)

    voice_question = voice_result["text"]
    voice_language = voice_result["language"]

    st.success(
        f"Recognized ({voice_language}) : {voice_question}"
    )

    translated_text = translate_to_english(
        voice_question
    )

    st.info(
        f"English Translation : {translated_text}"
    )
    
    if st.button("Use Voice Query"):

        st.session_state.voice_query = translated_text

# ================= FINAL QUESTION =================

question = None

if text_question and text_question.strip():

    question = text_question.strip()

elif st.session_state.voice_query:

    question = st.session_state.voice_query.strip()

if question:
    question = correct_company_names(question)

# ================= DUPLICATE PREVENTION =================

if question:

    if question == st.session_state.last_question:
        st.stop()

    st.session_state.last_question = question

# ================= QUESTION PROCESSING =================

# if question and len(question.strip()) >= 2:

#     question = normalize_query(question)

#     answer = None
#     docs = []
#     source = ""
if question and len(question.strip()) >= 2:

    question = normalize_query(question)

    result = graph.invoke(
        {
            "question": question,
            "retriever": st.session_state.retriever
        }
    )

    answer = result.get("answer")
    source = result.get("source", "unknown")
    docs = result.get("docs", [])

    st.session_state.chat_history.append(
        {
            "question": question,
            "answer": answer,
            "docs": docs,
            "source": source
        }
    )

    st.session_state.voice_query = None

    # ================= DATABASE TOOL =================

# ================= DISPLAY =================

for i, chat in enumerate(reversed(st.session_state.chat_history)):

    st.markdown("### ❓ Question")
    st.write(chat["question"])

    st.markdown("### 💡 Answer")

    st.markdown(
    f"""
    <div style="
        background-color:#E8F4FD;
        padding:20px;
        border-radius:15px;
        border-left:6px solid #1E88E5;
        color:#000000;
        font-size:17px;
        line-height:1.6;
        margin-bottom:10px;
    ">
    {str(chat["answer"]).replace(chr(10), "<br>")}
    </div>
    """,
    unsafe_allow_html=True
)

    st.caption(f"🔍 Source : {chat['source']}")

    if chat["docs"]:

        st.markdown("### 📄 Sources")

        pages = set()

        for d in chat["docs"]:

            page = d.metadata.get("page", "?")

            if page not in pages:

                pages.add(page)

                st.write(f"📌 Page {page}")

    st.divider()