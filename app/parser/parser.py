import re


from app.parser.aliases import ALIASES
from app.parser.reasons import REASONS
from app.parser.errors import (
    EmptyMessage,
    UnknownProduct,
    UnknownReason,
    InvalidQuantity,
)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def extract_multiplier(text: str):
    """
    Находит х2, x2, Х2
    """

    match = re.search(r"[xх]\s*(\d+)", text.lower())

    if match:
        multiplier = int(match.group(1))
        text = re.sub(r"[xх]\s*\d+", "", text, flags=re.IGNORECASE)
        return text.strip(), multiplier

    return text, 1


def extract_quantity(text: str):
    """
    Ищет количество списания.

    Правила:
    - если несколько чисел — количеством считается последнее;
    - если число сопровождается г/гр/мл/шт, единица удаляется;
    """

    matches = list(
        re.finditer(r"(\d+(?:[.,]\d+)?)\s*(г|гр|мл|шт)?", text.lower())
    )

    if not matches:
        return None, text

    match = matches[-1]

    quantity = float(match.group(1).replace(",", "."))

    start, end = match.span()

    text = text[:start] + text[end:]

    return quantity, text.strip()

def find_product(text: str):

    text = normalize(text)

    # 1. Точное совпадение
    if text in ALIASES:
        return ALIASES[text]

    # 2. Алиас полностью содержится в строке
    matches = []

    for alias, product in ALIASES.items():
        alias = normalize(alias)

        if alias in text:
            matches.append((len(alias), product))

    if matches:
        matches.sort(reverse=True)
        return matches[0][1]

    # 3. Строка полностью содержится в алиасе
    matches = []

    for alias, product in ALIASES.items():
        alias = normalize(alias)

        if text in alias:
            matches.append((len(alias), product))

    if matches:
        matches.sort()
        return matches[0][1]

    raise UnknownProduct(text)


def parse_item(line: str):

    line = normalize(line)

    line, multiplier = extract_multiplier(line)

    quantity, line = extract_quantity(line)

    if quantity is None:
        raise InvalidQuantity()

    # убираем лишние слова

    line = re.sub(r"\b(г|гр|мл|шт)\b", "", line)

    line = normalize(line)

    product = find_product(line)

    return {
        "product": product,
        "quantity": quantity * multiplier
    }

def parse_message(text: str):

    if not text.strip():
        raise EmptyMessage()

    lines = [
        normalize(i)
        for i in text.split("\n")
        if i.strip()
    ]

    action = "add"

    if lines[0] == "удали":
        action = "delete"
        lines.pop(0)

    elif lines[0] == "добавить":
        lines.pop(0)

    reason = None

    for i in range(len(lines) - 1, -1, -1):

        if lines[i] in REASONS:
            reason = lines.pop(i)
            break

    if reason is None:
        raise UnknownReason()

    items = []

    for line in lines:
        items.append(
            parse_item(line)
        )

    return {
        "action": action,
        "reason": reason,
        "items": items
    }