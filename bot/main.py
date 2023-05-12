import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.misc.env import Env

bot = Bot(token=Env.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")


async def on_start_up(dp: Dispatcher) -> None:
    logging.info("Bot launched successfully.")


def start_bot() -> None:
    executor.start_polling(dp, skip_updates=True, on_startup=on_start_up)
