from aiogram import types
from main_files.create_bot import bot
import emoji
from aiogram.utils.markdown import text, bold
from aiogram.types import ParseMode
from keyboards.main_kb import main_kb
from aiogram.dispatcher.filters.state import State, StatesGroup

users = {1413785229: text(bold("Лариса")), 297850814: text(bold("Маша"))}


def get_recipient_sender(id):
    sender = id
    if id == 1413785229:
        recipient = 297850814
    else:
        recipient = 1413785229
    return sender, recipient


class MainStates(StatesGroup):
    first_pg = State()


async def error(message: types.Message, e):
    temp_text = text(bold(message.from_user.username))
    await message.answer(
        emoji.emojize(':warning: Произошла какая-то ошибка. Подробности узнавайте у владельца бота!'),
        reply_markup=main_kb)
    await bot.send_message(chat_id='297850814', text=
    emoji.emojize(
        f':warning: В чате с пользователем @{temp_text} произошла '
        f'ошибка: \n' + str(e)), parse_mode=ParseMode.MARKDOWN)


# @dp.message_handler(lambda message: 'Отмена' in message.text)
async def cancel_cmd(message: types.Message):
    # await MainStates.first_page.set()
    await message.answer(emoji.emojize(f':check_mark_button: Отмена произведена'), reply_markup=main_kb)
