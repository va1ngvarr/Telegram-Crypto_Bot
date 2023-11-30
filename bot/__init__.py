import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import register_all_handlers
from database import register_all_models


storage = MemoryStorage()
dp = Dispatcher(storage=storage)


def start_bot(token: str) -> Bot:
    bot = Bot(token=token, parse_mode="HTML")

    async def on_startup() -> None:
        print("================================================")

        register_all_models()
        register_all_handlers(dp)

    dp.startup.register(on_startup)
    asyncio.run(dp.start_polling(bot, skip_updates=True))

    return bot
