import asyncio

from app.bot import bot, dp
from app.handlers.messages import router as messages_router
from app.handlers.edited_messages import router as edits_router


async def main():
    dp.include_router(messages_router)
    dp.include_router(edits_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())