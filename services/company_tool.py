from services.database_service import get_company_info


def company_tool(query):

    query = query.lower()

    company = None

    # TCS

    if "tcs" in query:
        company = "TCS"

    # Infosys

    elif "infosys" in query:
        company = "Infosys"

    # Wipro

    elif "wipro" in query:
        company = "Wipro"

    if company:

        data = get_company_info(company)

        if data:

            return f"""
Company: {data['company_name']}
CEO: {data['ceo']}
Eligibility: {data['eligibility']}
Package: {data['package']}
"""

    return None