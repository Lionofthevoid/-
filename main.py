import asyncio

from app.bot import bot, dp

from app.handlers.messages import router as message_router
from app.handlers.edited_messages import router as edited_router
from app.handlers.commands import router as command_router


async def main():
    dp.include_router(command_router)
    dp.include_router(edited_router)
    dp.include_router(message_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())