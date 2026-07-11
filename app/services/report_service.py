from collections import defaultdict

from app.database.writeoff_repository import get_report


def create_report():

    rows = get_report()

    if not rows:
        return "📋 За сегодня списаний нет."

    report = defaultdict(dict)

    for row in rows:
        report[row["reason"]][row["product"]] = row["quantity"]

    order = [
        "срок",
        "челфак",
        "обуч",
        "маркетинг",
        "нужды",
        "порча",
        "акция",
    ]

    text = "📋 Списания\n\n"

    # Сначала выводим причины в заданном порядке
    for reason in order:

        if reason not in report:
            continue

        text += f"{reason.capitalize()}\n"
        text += "──────────────\n"

        products = sorted(report[reason].items())

        for product, quantity in products:

            if quantity == int(quantity):
                quantity = int(quantity)

            text += f"{product} {quantity}\n"

        text += "\n"

    # Если появились новые причины, которых нет в списке order
    for reason in sorted(report.keys()):

        if reason in order:
            continue

        text += f"{reason.capitalize()}\n"
        text += "──────────────\n"

        products = sorted(report[reason].items())

        for product, quantity in products:

            if quantity == int(quantity):
                quantity = int(quantity)

            text += f"{product} {quantity}\n"

        text += "\n"

    return text