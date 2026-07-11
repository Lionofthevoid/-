from app.parser.parser import parse_message

from app.database.message_repository import (
    save_message,
    update_message,
    delete_message,
)

from app.database.writeoff_repository import (
    change_quantity,
    delete_items,
)


def _save_items(message_id: int, data: dict):
    """
    Сохраняет позиции с учетом действия:
    add -> +
    delete -> -
    """

    sign = 1

    if data["action"] == "delete":
        sign = -1

    change_quantity(
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

    data = parse_message(text)

    save_message(
        message_id=message_id,
        chat_id=chat_id,
        user_id=user_id,
        username=username,
        reason=data["reason"],
        message_text=text,
    )

    _save_items(message_id, data)

    return data


def edit_message(
    message_id: int,
    text: str,
):

    data = parse_message(text)

    delete_items(message_id)

    update_message(
        message_id=message_id,
        reason=data["reason"],
        message_text=text,
    )

    _save_items(message_id, data)

    return data


def remove_message(
    message_id: int,
):

    delete_items(message_id)

    delete_message(message_id)