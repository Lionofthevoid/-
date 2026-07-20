from datetime import datetime


def save_message(
    conn,
    message_id: int,
    chat_id: int,
    user_id: int,
    username: str | None,
    reason: str,
    message_text: str,
):
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


def get_message(conn, message_id: int):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM messages
        WHERE message_id = ?
    """, (message_id,))

    return cursor.fetchone()


def update_message(
    conn,
    message_id: int,
    reason: str,
    message_text: str,
):
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


def delete_message(conn, message_id: int):
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM messages
        WHERE message_id = ?
    """, (message_id,))
