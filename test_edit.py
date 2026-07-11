from app.parser.parser import parse_message
from app.database.db import (
    save_writeoff,
    delete_by_message_id,
    get_connection
)

# Первоначальное сообщение
text = """
мо 180
мк 190
Вышел срок годности
"""

data = parse_message(text)

save_writeoff(
    message_id=100,
    reason=data["reason"],
    items=data["items"]
)

print("Первое сообщение сохранено")


# Пользователь отредактировал сообщение
edited_text = """
мо 180
мк 200
Акция для клиентов
"""

# Удаляем старые записи этого сообщения
delete_by_message_id(100)

# Сохраняем новые
edited_data = parse_message(edited_text)

save_writeoff(
    message_id=100,
    reason=edited_data["reason"],
    items=edited_data["items"]
)

print("Сообщение обновлено")


# Проверяем содержимое БД
conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
    SELECT message_id, reason, product, quantity
    FROM writeoff_items
    WHERE message_id = 100
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()