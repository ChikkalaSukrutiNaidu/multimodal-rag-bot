from services.database_service import get_company_info

def company_tool(query):

    print("Inside company_tool")

    query = query.lower()

    company = None

    if "tcs" in query:
        company = "TCS"

    if company:
        print("Before DB Call")

        data = get_company_info(company)

        print("After DB Call")

        return str(data)

    return None