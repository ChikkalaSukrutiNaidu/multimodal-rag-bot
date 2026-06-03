from datetime import datetime

def date_tool(query):

    query = query.lower()

    if "date" in query:
        return datetime.now().strftime("%d-%m-%Y")

    if "time" in query:
        return datetime.now().strftime("%H:%M:%S")

    if "day" in query:
        return datetime.now().strftime("%A")

    return None