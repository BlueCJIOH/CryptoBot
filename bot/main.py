import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.handlers.exchanges import register_exchange_handlers
from bot.handlers.main import register_main_handlers
from bot.misc.env import Env

bot = Bot(token=Env.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")


async def on_start_up(dp: Dispatcher) -> None:
    logging.info("Bot launched successfully.")
    register_main_handlers(dp)
    register_exchange_handlers(dp)


def start_bot() -> None:
    executor.start_polling(dp, skip_updates=True, on_startup=on_start_up)
