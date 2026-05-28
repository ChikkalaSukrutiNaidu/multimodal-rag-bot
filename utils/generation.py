import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
You are an intelligent RAG assistant.

Rules:

1. Answer ONLY from the provided context.
2. If related information exists, infer carefully.
3. Do NOT unnecessarily say information is unavailable.
4. If truly unavailable say:
   "The uploaded document does not contain this information."
5. Keep answers short and accurate.
"""

def generate_answer(question, retriever):

    try:

        docs = retriever.invoke(question)

        if not docs:

            return (
                "The uploaded document does not contain this information.",
                []
            )

        context = "\n\n".join([

            f"""
Page: {d.metadata.get('page', '?')}

{d.page_content}
"""

            for d in docs

        ])

        final_prompt = f"""
Use the context carefully.

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