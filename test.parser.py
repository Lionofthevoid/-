from app.parser.parser import parse_message

text = """
удали

крышка 2 2
мк 110
нужды
"""

result = parse_message(text)

print(result)