from aiogram import Router
from aiogram.types import Message

from app.services.writeoff_service import edit_message
from app.utils.error_handler import format_error
from app.parser.message_detector import is_writeoff_message


router = Router()


@router.edited_message()
async def handle_edited(message: Message):

    if message.text is None:
        return

    if not is_writeoff_message(message.text):
        return

    try:

        edit_message(
            message_id=message.message_id,
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            username=message.from_user.username,
            text=message.text,
        )

        await message.reply(
            "✏️ Списание изменено"
        )

    except Exception as e:

        await message.reply(
            format_error(e)
        )
