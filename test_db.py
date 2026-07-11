from app.parser.parser import parse_message
from app.database.db import save_writeoff

text = """
мк 1440
экл 34
обуч
"""

data = parse_message(text)

save_writeoff(
    message_id=1,
    reason=data["reason"],
    items=data["items"]
)

print("Списание сохранено")