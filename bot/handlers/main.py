
from aiogram import Dispatcher
from aiogram.types import Message

from bot.keyboards.reply import exchange_keyboard


async def start(message: Message) -> None:
    await message.bot.send_message(
        message.from_user.id, text='Welcome to the CryptoBot!', reply_markup=exchange_keyboard
    )


def register_main_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(
        start,
        commands=[
            'start',
        ]
    )
