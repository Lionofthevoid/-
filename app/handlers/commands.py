from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.services.report_service import create_report
from app.database.writeoff_repository import delete_all
from app.keyboards.confirm_clear import confirm_clear_keyboard

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🤖 Бот учёта списаний\n\n"
        "Доступные команды:\n"
        "/report - показать отчёт\n"
        "/clear - удалить все списания за день\n"
        "/ping - проверить работу бота"
    )


@router.message(Command("ping"))
async def ping(message: Message):
    await message.answer("🏓 Pong")


@router.message(Command("report"))
async def report(message: Message):
    await message.answer(create_report())


@router.message(Command("clear"))
async def clear(message: Message):
    await message.answer(
        "⚠️ Вы действительно хотите удалить ВСЕ списания за сегодняшний день?\n\n"
        "Это действие нельзя отменить.",
        reply_markup=confirm_clear_keyboard,
    )


@router.callback_query(lambda c: c.data == "confirm_clear")
async def confirm_clear(callback: CallbackQuery):
    delete_all()

    await callback.message.edit_text(
        "✅ Все списания за день удалены!"
    )

    await callback.answer()


@router.callback_query(lambda c: c.data == "cancel_clear")
async def cancel_clear(callback: CallbackQuery):
    await callback.message.edit_text(
        "❎ Удаление отменено"
    )

    await callback.answer()