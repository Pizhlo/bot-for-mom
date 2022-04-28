from aiogram import types
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from main_files.create_bot import bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.db import add_new_card


class CardStates(StatesGroup):
    num_card = State()
    cvv = State()
    card_holder = State()
    date = State()

    num_card_text = ''
    cvv_text = ''
    card_holder_text = ''
    date_text = ''


# @dp.callback_query_handler(text='add_card') добавить карту
async def add_card(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введите номер карты: ', reply_markup=ReplyKeyboardRemove())
    await CardStates.num_card.set()


async def num_card(message: types.Message):
    CardStates.num_card_text = message.text
    await message.answer('Введите срок действия карты:')
    await CardStates.date.set()


async def date_card(message: types.Message):
    CardStates.date_text = message.text
    await message.answer('Введите cvv карты:')
    await CardStates.cvv.set()


async def cvv_card(message: types.Message):
    CardStates.cvv_text = message.text
    await message.answer('Введите владельца карты, как написано на ней:')
    await CardStates.card_holder.set()


async def card_holder_card(message: types.Message):
    CardStates.card_holder = message.text
    await add_new_card(message.from_user.id, CardStates.num_card_text, CardStates.card_holder_text,
                       CardStates.date_text, CardStates.cvv_text)


def card_handlers(dp):
    dp.register_callback_query_handler(add_card, text='add_card', state="*")

    dp.register_message_handler(num_card, state=CardStates.num_card)
    dp.register_message_handler(date_card, state=CardStates.date)
    dp.register_message_handler(cvv_card, state=CardStates.cvv)
    dp.register_message_handler(card_holder_card, state=CardStates.card_holder)
