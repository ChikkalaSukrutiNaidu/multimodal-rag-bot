import mysql.connector

def get_company_info(company):

    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="placement_db",
        port=3306
    )

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM company_info WHERE company_name=%s",
        (company,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result