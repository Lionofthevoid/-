from aiogram import Router
from aiogram.types import Message

from app.utils.error_handler import format_error
from app.services.writeoff_service import new_message
from app.parser.message_detector import is_writeoff_message

router = Router()


@router.message()
async def handle_message(message: Message):

    if message.text is None:
        return

    if not is_writeoff_message(message.text):
        return
    
    try:

        new_message(
            message_id=message.message_id,
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            username=message.from_user.username or "",
            text=message.text,
        )

        await message.reply("✅ Списание сохранено")

    except Exception as e:
        await message.reply(
            format_error(e)
        )