from app.parser.reasons import REASONS


def is_writeoff_message(text: str) -> bool:
    """
    Определяет, похоже ли сообщение на списание.
    """

    if not text:
        return False

    text = text.lower().strip()

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    if not lines:
        return False

    # Команда удаления
    if lines[0] == "удали":
        lines = lines[1:]

    # Команда добавления
    if lines and lines[0] == "добавить":
        lines = lines[1:]

    if not lines:
        return False

    # Последняя строка должна быть причиной списания
    if lines[-1] not in REASONS:
        return False

    # До причины должна быть хотя бы одна позиция
    return len(lines) >= 2