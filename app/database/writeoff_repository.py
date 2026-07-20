from app.database.db import get_connection


def save_items(conn, message_id: int, items: list):
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


def get_items(message_id: int):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT product, quantity
            FROM writeoff_items
            WHERE message_id = ?
        """, (message_id,))

        return cursor.fetchall()

    finally:
        conn.close()


def delete_items(conn, message_id: int):
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM writeoff_items
        WHERE message_id = ?
    """, (message_id,))


def delete_all():
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("DELETE FROM writeoff_items")
        cursor.execute("DELETE FROM messages")

        conn.commit()

    finally:
        conn.close()


def get_day_summary():
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                product,
                SUM(quantity)
            FROM writeoff_items
            GROUP BY product
            ORDER BY product
        """)

        return cursor.fetchall()

    finally:
        conn.close()


def get_report():
    conn = get_connection()

    try:
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

        return cursor.fetchall()

    finally:
        conn.close()


def change_quantity(conn, message_id: int, items: list, sign: int):
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
