from aiogram import types
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from main_files.create_bot import bot
from database.db import add_new_card
import sqlite3
from main_files.common import CardStates
import re


# @dp.callback_query_handler(text='add_card') добавить карту
async def add_card_inline(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await add_card_2(callback_query.from_user.id)


# @dp.message_handler(lambda message: 'Добавить карту' in message.text)
async def add_card(message: types.Message):
    await add_card_2(message.from_user.id)


# @dp.message_handler(lambda message: 'Удалить карту' in message.text)
async def delete_card(message: types.Message):
    connect = sqlite3.connect('C:\\Users\\1\\Desktop\\bot-for-mom\\database\\cards_db.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM cards WHERE user=?', (message.from_user.id,))
    check = cursor.fetchall()

    await message.answer('Выберите, какую карту хотите удалить (напишите цифрой):')
    i = 1
    for row in check:
        text = f'{i}. Номер карты: {row[1]}\n' \
               f'Владелец карты: {row[2]}\n' \
               f'CVV: {row[4]}\n' \
               f'Срок годности карты: {row[3]}'
        CardStates.card_dict[i] = row[1]
        i += 1
        await message.answer(text)
    await CardStates.number_to_delete.set()
    cursor.close()


async def add_card_2(user_id):
    await bot.send_message(user_id, 'Введите номер карты: ', reply_markup=ReplyKeyboardRemove())
    await CardStates.num_card.set()


async def num_card(message: types.Message):
    if re.match("[ - +]?\d+$", str(message)):
        CardStates.num_card_text = message.text
        await message.answer('Введите срок действия карты:')
        await CardStates.date.set()
    else:
        await message.answer('Некорректное значение. Ожидаются цифры.')


async def date_card(message: types.Message):
    CardStates.date_text = message.text
    await message.answer('Введите cvv карты:')
    await CardStates.cvv.set()


async def cvv_card(message: types.Message):
    CardStates.cvv_text = message.text
    await message.answer('Введите владельца карты, как написано на ней:')
    await CardStates.card_holder.set()


async def card_holder_card(message: types.Message):
    CardStates.card_holder_text = message.text
    await add_new_card(message.from_user.id, CardStates.num_card_text, CardStates.card_holder_text,
                       CardStates.date_text, CardStates.cvv_text)


def card_handlers(dp):
    dp.register_callback_query_handler(add_card_inline, text='add_card', state="*")

    dp.register_message_handler(add_card, lambda message: 'Добавить карту' in message.text, state="*")

    dp.register_message_handler(delete_card, lambda message: 'Удалить карту' in message.text, state="*")

    dp.register_message_handler(num_card, state=CardStates.num_card)
    dp.register_message_handler(date_card, state=CardStates.date)
    dp.register_message_handler(cvv_card, state=CardStates.cvv)
    dp.register_message_handler(card_holder_card, state=CardStates.card_holder)
