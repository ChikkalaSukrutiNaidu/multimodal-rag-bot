def calculator_tool(query):

    try:

        query = query.replace(" ", "")

        if any(op in query for op in ["+", "-", "*", "/"]):

            result = eval(query)

            return f"Result: {result}"

    except:
        return None

    return None