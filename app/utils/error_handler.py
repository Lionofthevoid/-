from app.parser.errors import (
    EmptyMessage,
    UnknownProduct,
    UnknownReason,
    InvalidQuantity,
)


def format_error(error: Exception) -> str:

    if isinstance(error, EmptyMessage):
        return (
            "❌ Сообщение пустое.\n\n"
            "Введите хотя бы одну позицию."
        )

    if isinstance(error, UnknownProduct):
        return (
            "❌ Неизвестный товар.\n\n"
            f"{error}"
        )

    if isinstance(error, UnknownReason):
        return (
            "❌ Не указана причина списания.\n\n"
            "Возможные причины:\n"
            "• срок\n"
            "• челфак\n"
            "• обуч\n"
            "• маркетинг\n"
            "• нужды\n"
            "• порча\n"
            "• акция"
        )

    if isinstance(error, InvalidQuantity):
        return (
            "❌ Не удалось определить количество."
        )

    return f"❌ Неизвестная ошибка:\n{error}"