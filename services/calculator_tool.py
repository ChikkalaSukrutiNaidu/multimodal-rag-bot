import re

def calculator_tool(query):

    try:

        query = query.lower()

        query = query.replace("plus", "+")
        query = query.replace("minus", "-")
        query = query.replace("times", "*")
        query = query.replace("multiplied by", "*")
        query = query.replace("x", "*")
        query = query.replace("divided by", "/")

        query = query.replace("is how much", "")
        query = query.replace("how much", "")
        query = query.replace("equals", "")
        query = query.replace("equal", "")
        query = query.replace("?", "")

        query = query.strip()

        if any(op in query for op in ["+", "-", "*", "/"]):

            expression = re.sub(
                r"[^0-9+\-*/(). ]",
                "",
                query
            )

            result = eval(expression)

            return f"Result: {result}"

    except Exception:
        return None

    return None