from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from main_files.common import MainStates
from keyboards.main_kb import main_kb
from keyboards.pulya_kb import pulya_kb_1, pulya_kb_2, pulya_6, back_button, question_inline_kb
from aiogram.utils.markdown import text, bold
from main_files.common import get_recipient_sender
from aiogram.types import ParseMode
import emoji
from main_files.create_bot import bot
from main_files.common import error, users
from aiogram.types import CallbackQuery


class PulyaStates(StatesGroup):
    first_pg = State()
    second_pg = State()
    wait_for_text = State()
    got_text = State()
    smiles_list = {text(bold('хочет есть')): ':cut_of_meat:',
                   text(bold('покушала')): ':face_savoring_food:',
                   text(bold('чихнула')): ':sneezing_face:',
                   text(bold('хочет играть')): ':zany_face:',
                   text(bold('играет')): ':squinting_face_with_tongue:',
                   text(bold('спрашивает')): ':white_question_mark:'
                   }


async def question(recipient):  # спрашивает хотите ли ответить на вопрос
    await bot.send_message(chat_id=recipient, text='Хотите ответить на этот вопрос?',
                           reply_markup=question_inline_kb)


# @dp.callback_query_handler(text='answer')
async def answer_yes(callback_query: CallbackQuery):  # если пользователь согласен ответить на уведомление
    await bot.answer_callback_query(callback_query.id)
    await PulyaStates.wait_for_text.set()
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await get_answer_text(callback_query.from_user.id)


async def get_answer_text(id):
    await bot.send_message(id, 'Введите ваш ответ. Для отмены напишите "отмена" ')
    await PulyaStates.got_text.set()


async def send_msg(message: types.Message):  # ответить на вопрос
    sender, recipient = get_recipient_sender(message.from_user.id)
    try:
        if message == 'отмена':
            await message.answer((emoji.emojize(':check_mark_button: "Отмена произведена"')), reply_markup=main_kb)
            await MainStates.first_pg.set()

            await bot.send_message(recipient, f'Пользователь {users[sender]} отказался отвечать на ваш вопрос.',
                                   parse_mode=ParseMode.MARKDOWN)
            return
        temp_text = text(bold('Текст сообщения:'))

        await bot.send_message(chat_id=recipient,
                               text=emoji.emojize(f':check_mark_button: Пользователь '
                                                  f'{users[sender]} ответил на ваш вопрос!'),
                               parse_mode=ParseMode.MARKDOWN)

        await bot.send_message(chat_id=recipient, text=f'{temp_text}  ', parse_mode=ParseMode.MARKDOWN)
        await bot.send_message(chat_id=recipient, text=message.text, parse_mode=ParseMode.MARKDOWN)
        await message.answer(emoji.emojize(f':check_mark_button: Ваш ответ успешно отправлен!'),
                             reply_markup=main_kb,
                             parse_mode=ParseMode.MARKDOWN)
        await MainStates.first_pg.set()
    except Exception as e:

        await error(message, e)


# @dp.callback_query_handler(text='dont_answer')
async def answer_no(callback_query: CallbackQuery):  # если пользователь не согласен ответить на уведомление
    await bot.answer_callback_query(callback_query.id)
    sender, recipient = get_recipient_sender(callback_query.from_user.id)
    await bot.send_message(recipient,
                           emoji.emojize(f'Пользователь {users[sender]} отказался отвечать на ваш вопрос.'),
                           parse_mode=ParseMode.MARKDOWN)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(recipient, emoji.emojize(f':check_mark_button: Ваш ответ успешно отправлен!'),
                           reply_markup=main_kb,
                           parse_mode=ParseMode.MARKDOWN)


async def send_msg_type_1(message: types.Message, msg, notif_msg):
    sender, recipient = get_recipient_sender(message.from_user.id)
    try:
        if msg == text(bold('спрашивает')):
            await bot.send_message(chat_id=recipient,
                                   text=emoji.emojize(f'Пользователь {users[sender]} {msg} у '
                                                      f'пользователя {users[recipient]}, что делает Плюпка! {PulyaStates.smiles_list[msg]}'),
                                   parse_mode=ParseMode.MARKDOWN)
            await question(recipient)
            await message.answer(emoji.emojize(f':check_mark_button: Сообщение {notif_msg} '
                                               'успешно отправлено!'), reply_markup=main_kb,
                                 parse_mode=ParseMode.MARKDOWN)
        else:
            await bot.send_message(chat_id=recipient,
                                   text=emoji.emojize(f'Пользователь {users[sender]} передает '
                                                      f'пользователю {users[recipient]}, что Плюпка {msg}! {PulyaStates.smiles_list[msg]}'),
                                   parse_mode=ParseMode.MARKDOWN)
            await message.answer(emoji.emojize(f':check_mark_button: Сообщение "{text(bold("Плюпка"))} {notif_msg}" '
                                               'успешно отправлено!'), reply_markup=main_kb,
                                 parse_mode=ParseMode.MARKDOWN)

        await MainStates.first_pg.set()

    except Exception as e:

        await error(message, e)


# @dp.message_handler(lambda message: 'хочет есть' in message.text)
async def wanna_eat_cmd(message: types.Message):
    msg = text(bold('хочет есть'))
    notif_msg = text(bold('хочет есть'))
    await send_msg_type_1(message, msg, notif_msg)


# @dp.message_handler(lambda message: 'покушала' in message.text)
async def has_eaten_cmd(message: types.Message):
    msg = text(bold('покушала'))
    notif_msg = text(bold('покушала'))
    await send_msg_type_1(message, msg, notif_msg)


# @dp.message_handler(lambda message: 'чихнула' in message.text)
async def sneeze_cmd(message: types.Message):
    msg = text(bold('чихнула'))
    notif_msg = text(bold('чихнула'))
    await send_msg_type_1(message, msg, notif_msg)


# @dp.message_handler(lambda message: 'хочет играть' in message.text)
async def wanna_play_cmd(message: types.Message):
    msg = text(bold('хочет играть'))
    notif_msg = text(bold('хочет играть'))
    await send_msg_type_1(message, msg, notif_msg)


# @dp.message_handler(lambda message: 'играет' in message.text)
async def is_playing_cmd(message: types.Message):
    msg = text(bold('играет'))
    notif_msg = text(bold('играет'))
    await send_msg_type_1(message, msg, notif_msg)


# @dp.message_handler(lambda message: 'спросить' in message.text)
async def ask_cmd(message: types.Message):
    msg = text(bold('спрашивает'))
    notif_msg = text(bold("Что делает Плюпка?"))
    await send_msg_type_1(message, msg, notif_msg)


# lambda message: 'Назад' in message.text, state=PulyaStates.first_pg
async def come_back(message: types.Message):
    await MainStates.first_pg.set()
    await message.answer('Выбери вариант', reply_markup=main_kb)


# lambda message: 'Назад' in message.text, state=PulyaStates.second_pg
async def first_pg(message: types.Message):
    await PulyaStates.first_pg.set()
    await message.answer('Выбери вариант', reply_markup=pulya_kb_1)


# lambda message: 'Далее' in message.text, state=PulyaStates.first_pg
async def second_pg(message: types.Message):
    await PulyaStates.second_pg.set()
    if message.from_user.id == 297850814:
        pulya_kb_2.add(pulya_6)
    else:
        pass
    pulya_kb_2.add(back_button)
    await message.answer('Выбери вариант', reply_markup=pulya_kb_2)


def pulya_handlers(dp):
    dp.register_message_handler(come_back, lambda message: 'Назад' in message.text, state=PulyaStates.first_pg)
    dp.register_message_handler(first_pg, lambda message: 'Назад' in message.text, state=PulyaStates.second_pg)
    dp.register_message_handler(second_pg, lambda message: 'Далее' in message.text, state=PulyaStates.first_pg)

    dp.register_message_handler(wanna_eat_cmd, lambda message: 'хочет есть' in message.text, state="*")
    dp.register_message_handler(has_eaten_cmd, lambda message: 'покушала' in message.text, state="*")
    dp.register_message_handler(sneeze_cmd, lambda message: 'чихнула' in message.text, state="*")
    dp.register_message_handler(wanna_play_cmd, lambda message: 'хочет играть' in message.text, state="*")
    dp.register_message_handler(is_playing_cmd, lambda message: 'играет' in message.text, state="*")
    dp.register_message_handler(ask_cmd, lambda message: 'Спросить' in message.text, state="*")

    # inline button

    dp.register_callback_query_handler(answer_yes, text='answer', state="*")
    dp.register_callback_query_handler(answer_no, text='dont_answer', state="*")

    dp.register_message_handler(get_answer_text, state=PulyaStates.wait_for_text)
    dp.register_message_handler(send_msg, state=PulyaStates.got_text)
