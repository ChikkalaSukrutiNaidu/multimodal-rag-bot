import mysql.connector

print("Connecting...")

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="placement_db",
    port=3306,
    connection_timeout=5
)

print("Connected")

conn.close()