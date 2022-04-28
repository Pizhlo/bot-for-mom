from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils.markdown import text, bold, italic
from aiogram.types import CallbackQuery
from main_files.create_bot import bot
import emoji
from keyboards.main_kb import main_kb
from main_files.common import users
from main_files.common import MainStates
from keyboards.money_kb import result_kb, money_kb, change_request_kb
from aiogram.types import ReplyKeyboardRemove


class MoneyStates(StatesGroup):
    target = State()
    amount = State()
    result = State()

    change_target = State()
    change_amount = State()

    target_text = ''
    amount_text = ''


async def make_money_request(message: types.Message):
    MoneyStates.target_text = message.text
    await message.answer('Введите необходимую сумму: ')
    await MoneyStates.amount.set()


async def get_amount(message: types.Message):
    MoneyStates.amount_text = message.text
    await MoneyStates.result.set()
    await result(message)


async def result(message: types.Message):
    await message.answer(
        f'Проверьте запрос:\n{text(italic("Цель:"))} {MoneyStates.target_text}\n{text(italic("Сумма:"))} '
        f'{MoneyStates.amount_text}',
        parse_mode=ParseMode.MARKDOWN)
    await message.answer('Все верно?', reply_markup=result_kb)


# @dp.callback_query_handler(text='send_request') отправить запрос на финансирование
async def send_request(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(297850814, emoji.emojize(f':check_mark_button: Ваш запрос успешно отправлен!'),
                           reply_markup=main_kb,
                           parse_mode=ParseMode.MARKDOWN)
    await MainStates.first_pg.set()
    await bot.send_message(1413785229, emoji.emojize(f'Пользователь '
                                                     f'{users[297850814]} прислал вам '
                                                     f'запрос на финансирование! :dollar_banknote:'),
                           parse_mode=ParseMode.MARKDOWN)

    await bot.send_message(1413785229,
                           f'{text(bold("Запрос на финансирование"))}\n{text(italic("Цель:"))} {MoneyStates.target_text}\n{text(italic("Сумма:"))} {MoneyStates.amount_text}\n'
                           'Отправить деньги?',
                           parse_mode=ParseMode.MARKDOWN, reply_markup=money_kb)
    del MoneyStates.amount_text
    del MoneyStates.target_text
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)


# @dp.callback_query_handler(text='change_request') изменить запрос на финансирование
async def change_request(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(297850814, 'Выберете, что нужно изменить:', reply_markup=change_request_kb)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)


# @dp.callback_query_handler(text='change_amount') изменить запрос на финансирование (сумма)
async def change_amount(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await MoneyStates.change_amount.set()
    await bot.send_message(297850814, 'Введите новое значение:', reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)


# @dp.callback_query_handler(text='change_target') изменить запрос на финансирование (цель)
async def change_target(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await MoneyStates.change_target.set()
    await bot.send_message(297850814, 'Введите новое значение:', reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)


# state = MoneyStates.change_amount
async def new_amount(message: types.Message):
    MoneyStates.amount_text = message.text
    await MoneyStates.result.set()
    await result(message)


# state = MoneyStates.change_target
async def new_target(message: types.Message):
    MoneyStates.target_text = message.text
    await MoneyStates.result.set()
    await result(message)


def money_handlers(dp):
    dp.register_message_handler(make_money_request, state=MoneyStates.target)
    dp.register_message_handler(get_amount, state=MoneyStates.amount)

    # отправить запрос

    dp.register_callback_query_handler(send_request, text='send_request', state="*")

    # изменить запрос

    dp.register_callback_query_handler(change_request, text='change_request', state="*")
    dp.register_callback_query_handler(change_amount, text='change_amount', state="*")
    dp.register_callback_query_handler(change_target, text='change_target', state="*")

    # новые значения запроса

    dp.register_message_handler(new_amount, state=MoneyStates.change_amount)
    dp.register_message_handler(new_target, state=MoneyStates.change_target)
