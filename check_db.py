from app.database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
    SELECT *
    FROM writeoff_items
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()