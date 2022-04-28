from aiogram import types
from main_files.common import MainStates
from keyboards.main_kb import main_kb
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.markdown import text, bold
from main_files.common import error, users, get_recipient_sender
from main_files.create_bot import bot
import emoji
from aiogram.types import ParseMode
from keyboards.geo_kb import geo_kb
from handlers.money_handler import MoneyStates
from aiogram.types import ReplyKeyboardRemove


class RequestStates(StatesGroup):
    first_pg = State()

    smiles_list = {
        text(bold('запрашивает геолокацию')): ':compass:'
    }


# @dp.message_handler(lambda message: 'Запрос геолокации' in message.text)
async def get_geo(message: types.Message):
    temp_text = text(bold('запрашивает геолокацию'))
    sender, recipient = get_recipient_sender(message.from_user.id)
    try:

        await bot.send_message(chat_id=recipient,
                               text=emoji.emojize(f'Пользователь {users[sender]} {temp_text} '
                                                  f'у пользователя {users[recipient]}. {RequestStates.smiles_list[temp_text]}\n'
                                                  ' Поделиться геолокацией?'), reply_markup=geo_kb,
                               parse_mode=ParseMode.MARKDOWN)
        temp_text = text(bold('геолокации'))
        await message.answer(emoji.emojize(f':check_mark_button: Запрос {temp_text} успешно отправлен!'),
                             reply_markup=main_kb, parse_mode=ParseMode.MARKDOWN)
        await MainStates.first_pg.set()
    except Exception as e:

        await error(message, e)


# @dp.callback_query_handler(lambda message: 'Отказаться' in message.text, state="*")
async def not_send_geo(message: types.Message):
    temp_text = text(bold('отказался'))
    sender, recipient = get_recipient_sender(message.from_user.id)
    await bot.send_message(chat_id=recipient, text=emoji.emojize(f':warning: К сожалению, пользователь '
                                                                 f'{users[sender]} '
                                                                 f'{temp_text} поделиться своей геолокацией.'),
                           parse_mode=ParseMode.MARKDOWN)


# @dp.message_handler(content_types=['location'])
async def do_send_geo(message: types.Message):
    temp_text = text(bold('согласился'))
    try:
        lat = message.location.latitude
        lon = message.location.longitude
        sender, recipient = get_recipient_sender(message.from_user.id)

        await bot.send_message(chat_id=recipient,
                               text=emoji.emojize(f':check_mark_button: Пользователь {users[sender]} '
                                                  f'{temp_text} поделиться своей геолокацией!'),
                               parse_mode=ParseMode.MARKDOWN)

        await bot.send_location(chat_id=recipient, latitude=lat, longitude=lon, reply_markup=main_kb)

        await bot.send_message(sender,
                               emoji.emojize(":check_mark_button: Геолокация успешно отправлена!"),
                               reply_markup=main_kb)

        await MainStates.first_pg.set()

    except Exception as e:

        await error(message, e)


# @dp.message_handler(lambda message: 'Запрос на финансирование' in message.text)
async def money_cmd(message: types.Message):
    await message.answer('Введите цель финансирования: ', reply_markup=ReplyKeyboardRemove())
    await MoneyStates.target.set()


# lambda message: 'Назад' in message.text, state=PulyaStates.first_pg
async def come_back(message: types.Message):
    await MainStates.first_pg.set()
    await message.answer('Выбери вариант', reply_markup=main_kb)


def requests_handlers(dp):
    dp.register_message_handler(come_back, lambda message: 'Назад' in message.text, state=RequestStates.first_pg)

    dp.register_message_handler(get_geo, lambda message: 'Запрос геолокации' in message.text,
                                state=RequestStates.first_pg)
    # геолокация

    dp.register_message_handler(not_send_geo, lambda message: 'Отказаться' in message.text, state="*")
    dp.register_message_handler(do_send_geo, content_types=['location'], state="*")

    # финансирование

    dp.register_message_handler(money_cmd, lambda message: 'Запрос на финансирование' in message.text, state="*")
