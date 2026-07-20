from app.parser.parser import parse_message

from app.database.db import get_connection

from app.database.message_repository import (
    save_message,
    get_message,
    update_message,
    delete_message,
)

from app.database.writeoff_repository import (
    change_quantity,
    delete_items,
)


def _save_items(conn, message_id: int, data: dict):
    """
    Сохраняет позиции с учетом действия:
    add -> +
    delete -> -
    """

    sign = 1

    if data["action"] == "delete":
        sign = -1

    change_quantity(
        conn=conn,
        message_id=message_id,
        items=data["items"],
        sign=sign,
    )


def new_message(
    message_id: int,
    chat_id: int,
    user_id: int,
    username: str,
    text: str,
):
    conn = get_connection()

    try:
        data = parse_message(text)

        save_message(
            conn=conn,
            message_id=message_id,
            chat_id=chat_id,
            user_id=user_id,
            username=username,
            reason=data["reason"],
            message_text=text,
        )

        _save_items(conn, message_id, data)

        conn.commit()

        return data

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def edit_message(
    message_id: int,
    chat_id: int,
    user_id: int,
    username: str | None,
    text: str,
):
    conn = get_connection()

    try:
        data = parse_message(text)

        old_message = get_message(
            conn=conn,
            message_id=message_id,
        )

        # Если сообщение уже есть в базе
        if old_message is not None:

            # Удаляем старые позиции
            delete_items(
                conn=conn,
                message_id=message_id,
            )

            # Обновляем причину и текст
            update_message(
                conn=conn,
                message_id=message_id,
                reason=data["reason"],
                message_text=text,
            )

            # Добавляем новые позиции
            _save_items(
                conn=conn,
                message_id=message_id,
                data=data,
            )

        # Если сообщения ещё нет в базе
        else:

            save_message(
                conn=conn,
                message_id=message_id,
                chat_id=chat_id,
                user_id=user_id,
                username=username,
                reason=data["reason"],
                message_text=text,
            )

            _save_items(
                conn=conn,
                message_id=message_id,
                data=data,
            )

        conn.commit()

        return data

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def remove_message(
    message_id: int,
):
    conn = get_connection()

    try:
        delete_items(
            conn=conn,
            message_id=message_id,
        )

        delete_message(
            conn=conn,
            message_id=message_id,
        )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
