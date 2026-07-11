from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


confirm_clear_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Да, удалить",
                callback_data="confirm_clear"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Отмена",
                callback_data="cancel_clear"
            )
        ]
    ]
)