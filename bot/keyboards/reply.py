from typing import Final

from aiogram.types import ReplyKeyboardMarkup

from bot.misc.util import exchange_list

keyboard: Final = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

exchange_keyboard: Final = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

exchange_keyboard.add(*exchange_list)

action_keyboard: Final = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

action_keyboard.add("Currencies", "Get a Price", "Price Log", "Back")
