chat_memory = []


def save_chat(question, answer):

    chat_memory.append(
        {
            "question": question,
            "answer": answer
        }
    )

    if len(chat_memory) > 5:
        chat_memory.pop(0)


def get_history():

    text = ""

    for item in chat_memory:

        text += f"""
Question:
{item['question']}

Answer:
{item['answer']}
"""

    return text