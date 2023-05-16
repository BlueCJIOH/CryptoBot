import logging

import requests
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.keyboards.reply import action_keyboard, exchange_keyboard
from bot.misc.util import exchange_list
from bot.states.states import UserStatesGroup


async def set_price_state(message: Message, state: FSMContext) -> None:
    await UserStatesGroup.next()
    await message.bot.send_message(
        message.from_user.id,
        text="Write the name of a certain currency you wanna know",
        reply_markup=ReplyKeyboardRemove()
    )


async def get_currency_price(message: Message, state: FSMContext) -> None:
    # TODO: check the case if it's Common log
    data = await state.get_data()
    rq = requests.post(
        "http://web:8000/exchanges/currency_by_name_from/",
        json={"name": data['exchange'], "cname": message.text}
    ).json()[data['exchange']]
    if rq['name'] != 'Not found':
        txt = f"{rq['name']}: {rq['price']}"
        await message.bot.send_message(
            message.from_user.id,
            text=f'{txt}\n'
                 'Select an item from the menu',
            reply_markup=action_keyboard
        )
    else:
        await message.bot.send_message(
            message.from_user.id,
            text='The name of a currency wasn\'t found.\n'
                 'Select an item from the menu',
            reply_markup=action_keyboard
        )
    await UserStatesGroup.item.set()


async def list_currencies(message: Message, state: FSMContext) -> None:
    # TODO: check the case if it's Common log
    data = await state.get_data()
    rq = requests.post(
        "http://web:8000/exchanges/currency_names_from/",
        json={"name": data['exchange']}
    ).json()[data['exchange']]
    txt = '\n'.join(rq)
    await message.bot.send_message(
        message.from_user.id,
        text=txt,
        reply_markup=action_keyboard
    )


async def list_prices(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if data['exchange'] == 'Common log':
        rq = requests.get(
            "http://web:8000/exchanges/all_currencies/",
        ).json()
        txt = ''
        for el in rq:
            txt += '\n\n' + '*' + str(list(el.keys())[0]) + '*' + '\n'
            for foo in el.values():
                txt += '\n'.join(list(map(lambda bar: f'{bar["name"]}: {bar["price"]}', foo)))
    else:
        rq = requests.post(
            "http://web:8000/exchanges/currencies_by_name/",
            json={"name": data['exchange']}
        ).json()[data['exchange']]
        txt = '\n'.join(list(map(lambda el: f'{el["name"]}: {el["price"]}', rq)))
    await message.bot.send_message(
        message.from_user.id,
        text=txt,
        reply_markup=action_keyboard,
        parse_mode='Markdown'
    )


async def move_back(message: Message, state: FSMContext) -> None:
    await state.finish()
    await message.bot.send_message(message.from_user.id, text="Select an exchange from the menu",
                                   reply_markup=exchange_keyboard)


async def select(message: Message, state: FSMContext) -> None:
    try:
        await select_dict.get(message.text)(message, state)
    except KeyError:
        await message.bot.send_message(message.from_user.id, text="Select an item from the menu",
                                       reply_markup=action_keyboard)


async def text(message: Message, state: FSMContext) -> None:
    try:
        if message.text in exchange_list:
            await UserStatesGroup.item.set()
            async with state.proxy() as data:
                data["exchange"] = message.text
            await message.bot.send_message(message.from_user.id, text="Select an item from the menu",
                                           reply_markup=action_keyboard)
            return
        await message.bot.send_message(message.from_user.id, text="Select an exchange from the menu",
                                       reply_markup=exchange_keyboard)
    except:
        logging.warning("Something is wrong!")
        await message.bot.send_message(message.from_user.id, text="Select an exchange from the menu",
                                       reply_markup=action_keyboard)


select_dict = {
    'Currencies': list_currencies,
    'Get a Price': set_price_state,
    'Price Log': list_prices,
    'Back': move_back,
}


def register_exchange_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(
        text,
        content_types=['text', ],
        state=None
    )
    dp.register_message_handler(
        select,
        content_types=['text', ],
        state=UserStatesGroup.item
    )
    dp.register_message_handler(
        get_currency_price,
        content_types=['text', ],
        state=UserStatesGroup.currency
    )
