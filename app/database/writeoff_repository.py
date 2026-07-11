from app.database.db import get_connection


def save_items(message_id: int, items: list):
    conn = get_connection()
    cursor = conn.cursor()

    for item in items:
        cursor.execute("""
            INSERT INTO writeoff_items (
                message_id,
                product,
                quantity
            )
            VALUES (?, ?, ?)
        """, (
            message_id,
            item["product"],
            item["quantity"]
        ))

    conn.commit()
    conn.close()


def get_items(message_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT product, quantity
        FROM writeoff_items
        WHERE message_id = ?
    """, (message_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def delete_items(message_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM writeoff_items
        WHERE message_id = ?
    """, (message_id,))

    conn.commit()
    conn.close()


def delete_all():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM writeoff_items")
    cursor.execute("DELETE FROM messages")

    conn.commit()
    conn.close()


def get_day_summary():
    """
    Возвращает сумму по каждому товару.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            product,
            SUM(quantity)
        FROM writeoff_items
        GROUP BY product
        ORDER BY product
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def get_report():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            messages.reason,
            writeoff_items.product,
            SUM(writeoff_items.quantity) as quantity
        FROM writeoff_items
        JOIN messages
            ON messages.message_id = writeoff_items.message_id
        GROUP BY
            messages.reason,
            writeoff_items.product
        ORDER BY
            messages.reason,
            writeoff_items.product
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def change_quantity(message_id: int, items: list, sign: int):
    """
    sign = 1  -> добавить
    sign = -1 -> вычесть
    """

    conn = get_connection()
    cursor = conn.cursor()

    for item in items:

        cursor.execute("""
            INSERT INTO writeoff_items (
                message_id,
                product,
                quantity
            )
            VALUES (?, ?, ?)
        """, (
            message_id,
            item["product"],
            item["quantity"] * sign
        ))

    conn.commit()
    conn.close()