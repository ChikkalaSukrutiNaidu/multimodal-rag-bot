import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
You are a helpful RAG AI assistant.

Rules:
1. Answer ONLY from provided context.
2. If answer is unavailable, say:
   "The uploaded documents do not contain this information."
3. Give clear and direct answers.
4. Use the most relevant retrieved content.
5. Mention source pages naturally.
"""

def generate_answer(question, retriever):

    try:

        docs = retriever.invoke(question)

        if not docs:
            return (
                "The uploaded documents do not contain this information.",
                []
            )

        seen = set()
        unique_docs = []

        for d in docs:

            key = (
                d.metadata.get("source", "Unknown"),
                d.metadata.get("page", "?")
            )

            if key not in seen:
                seen.add(key)
                unique_docs.append(d)

        docs = unique_docs

        context = "\n\n".join(
            f"""
Source: {d.metadata.get('source', 'Unknown')}
Page: {d.metadata.get('page', '?')}

Content:
{d.page_content}
"""
            for d in docs
        )

        final_prompt = f"""
CONTEXT:

{context}

QUESTION:
{question}

ANSWER:
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": final_prompt
                }
            ],
            temperature=0
        )

        answer = response.choices[0].message.content

        return answer, docs

    except Exception as e:

        return f"Error: {str(e)}", []