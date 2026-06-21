from graph import state
from services.llm_service import llm
from services.ipl_stats_tool import is_ipl_stats_query
from services.company_tool import company_tool
from services.rag_service import ask_question
from services.web_search_tool import tavily_search
from services.calculator_tool import calculator_tool
from services.date_tool import date_tool
from services.memory import get_history
from services.relevance_checker import is_relevant

def router_node(state):

    question = state["question"].lower()

    reasoning_keywords = [
    "compare",
    "difference",
    "both",
    "highest and",
    "most runs and",
    "most wickets and",
    "top batsman and top bowler",
    "better",
    "average",
    "he",
    "him",
    "his",
    "they",
    "them",
    "that player",
    "that team",
    "centuries",
"matches",
"strike rate",
"average",
"runs",
"wickets"
]

    if any(keyword in question for keyword in reasoning_keywords):
        return {"route": "reasoning"}

    temporal_keywords = [
        "between",
        "from",
        "after",
        "before",
        "since",
        "during",
        "2018",
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024",
        "2025",
        "2026"
    ]

    if any(keyword in question for keyword in temporal_keywords):
        return {"route": "temporal"}
    

    if any(
        word in question
        for word in [
            "ceo",
            "package",
            "eligibility",
            "company"
        ]
    ):
        return {"route": "company"}

    if any(
        word in question
        for word in [
            "calculate",
            "plus",
            "minus",
            "times",
            "divided",
            "+",
            "-",
            "*",
            "/"
        ]
    ):
        return {"route": "calculator"}

    if any(
        word in question
        for word in [
            "today",
            "date",
            "day",
            "month",
            "year"
        ]
    ):
        return {"route": "date"}
    if any(
    word in question
    for word in [
        "ipl",
        "rcb",
        "csk",
        "mi",
        "mumbai indians",
        "kkr",
        "rr",
        "gt",
        "pbks",
        "srh",
        "dc",
        "lsg"
    ]
):
        return {"route": "ipl_stats"}
    if any(
        word in question
        for word in [
            "latest",
            "news",
            "current",
            "recent",
            "2025",
            "2026",
            "winner",
            "won",
            "points table",
            "orange cap",
            "purple cap"
        ]
    ):
        return {"route": "web"}

    if is_ipl_stats_query(question):
        return {"route": "ipl_stats"}

    if state["retriever"] is not None:
        return {"route": "rag"}

    return {"route": "web"}


def company_node(state):

    answer = company_tool(state["question"])

    return {
        "answer": answer,
        "source": "database",
        "docs": []
    }


def calculator_node(state):

    answer = calculator_tool(state["question"])

    return {
        "answer": answer,
        "source": "calculator",
        "docs": []
    }


def date_node(state):

    answer = date_tool(state["question"])

    return {
        "answer": answer,
        "source": "date",
        "docs": []
    }


def rag_node(state):

    retriever = state["retriever"]

    if retriever is None:
        return {
            "answer": "IPL dataset not loaded.",
            "source": "pdf_rag",
            "docs": []
        }

    answer, docs = ask_question(
        state["question"],
        retriever
    )

    return {
        "answer": answer,
        "source": "pdf_rag",
        "docs": docs
    }

def ipl_stats_node(state):

    retriever = state["retriever"]

    if retriever is None:
        return {
            "answer": "IPL dataset not loaded.",
            "source": "ipl_stats",
            "docs": []
        }

    results = retriever.vectorstore.similarity_search_with_score(
        state["question"],
        k=4
    )

    docs = [doc for doc, score in results]
    scores = [score for doc, score in results]

    print("IPL Stats Scores:", scores)

    if not is_relevant(scores):
        return web_node(state)

    answer, docs = ask_question(
        state["question"],
        retriever
    )

    return {
        "answer": answer,
        "source": "ipl_stats",
        "docs": docs
    }






def reasoning_node(state):

    retriever = state["retriever"]

    if retriever is None:
        return {
            "answer": "IPL dataset not loaded.",
            "source": "reasoning",
            "docs": []
        }

    docs = retriever.invoke(
        state["question"]
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    history = state.get(
        "history",
        ""
    )

    response = llm.invoke(
        f"""
You are an IPL analytics assistant.

Previous Conversation:
{history}

IPL Context:
{context}

Current Question:
{state['question']}

Rules:

1. Use Previous Conversation to resolve references.

2. If user says:
   - he
   - him
   - his
   - they
   - them
   - that player
   - that team

   identify the entity ONLY from Previous Conversation.

3. If the previous conversation contains a comparison between players,
   and the current question is a follow-up,
   answer ONLY about those compared players.

4. Never introduce a new player from IPL Context.

Example:

User: Compare Virat Kohli and Rohit Sharma

User: Who has better average?

Correct:
Virat Kohli has a better average (37.17) than Rohit Sharma (29.57).

Wrong:
KL Rahul has the highest average.

User: How many centuries does he have?

Correct:
Virat Kohli has 7 centuries.

5. Answer only from IPL Context.

6. Maximum 3 lines.

Final Answer:
"""
    )

    return {
        "answer": response.content,
        "source": "reasoning",
        "docs": docs
    }
def temporal_node(state):

    retriever = state["retriever"]

    docs = retriever.invoke(state["question"])

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    history = state.get("history", "")

    response = llm.invoke(
        f"""
You are an IPL temporal reasoning assistant.

Previous Conversation:
{history}

IPL Context:
{context}

Current Question:
{state['question']}

Rules:

1. Use Previous Conversation.

2. Resolve references like:
   - before that
   - after that
   - that year
   - previous season
   - next season

3. Example:

User: Who won IPL in 2023?
Answer: CSK

User: Who won before that?

Answer: GT won IPL 2022.

4. Answer only from IPL Context.

5. Maximum 3 lines.

Final Answer:
"""
    )

    return {
        "answer": response.content,
        "source": "temporal",
        "docs": docs
    }

def web_node(state):

    question = state["question"]

    web_content = tavily_search(question)

    if not web_content:
        return {
            "answer": "No web results found.",
            "source": "web",
            "docs": []
        }

    summary = llm.invoke(
        f"""
        User Question:
        {question}

        Web Search Results:
        {web_content}

        Rules:
        - Give only the final answer.
        - Maximum 5 lines.
        - Do not copy website content.
        - Summarize important facts only.
        """
    )

    return {
        "answer": summary.content,
        "source": "web",
        "docs": []
    }