from datetime import datetime

from app.database.db import get_connection


def save_message(
    message_id: int,
    chat_id: int,
    user_id: int,
    username: str | None,
    reason: str,
    message_text: str,
):
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now().isoformat(timespec="seconds")

    cursor.execute("""
        INSERT INTO messages (
            message_id,
            chat_id,
            user_id,
            username,
            reason,
            message_text,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        message_id,
        chat_id,
        user_id,
        username,
        reason,
        message_text,
        now,
        now
    ))

    conn.commit()
    conn.close()


def get_message(message_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM messages
        WHERE message_id = ?
    """, (message_id,))

    message = cursor.fetchone()

    conn.close()

    return message


def update_message(
    message_id: int,
    reason: str,
    message_text: str,
):
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now().isoformat(timespec="seconds")

    cursor.execute("""
        UPDATE messages
        SET
            reason = ?,
            message_text = ?,
            updated_at = ?
        WHERE message_id = ?
    """, (
        reason,
        message_text,
        now,
        message_id
    ))

    conn.commit()
    conn.close()


def delete_message(message_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM messages
        WHERE message_id = ?
    """, (message_id,))

    conn.commit()
    conn.close()