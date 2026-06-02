import mysql.connector

print("Starting")

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="placement_db",
    port=3306
)

print("Connected")

cursor = conn.cursor(dictionary=True)

cursor.execute(
    "SELECT * FROM company_info WHERE company_name=%s",
    ("TCS",)
)

data = cursor.fetchone()

print(data)

cursor.close()
conn.close()