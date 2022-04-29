import sqlite3
from main_files.create_bot import bot
from keyboards.main_kb import main_kb
import emoji
from main_files.common import MainStates
from aiogram import types
from main_files.common import CardStates
from main_files.common import error


# добавить новую карту
async def add_new_card(user_id, card_number, cardholder, date, cvv):
    arr = (user_id, card_number, cardholder, date, cvv)
    connect = sqlite3.connect('C:\\Users\\1\\Desktop\\bot-for-mom\\database\\cards_db.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO cards VALUES(?, ?, ?, ?, ?)', (user_id, card_number, cardholder, date, cvv))
    connect.commit()
    cursor.close()
    await bot.send_message(user_id, emoji.emojize(':check_mark_button: Ваша карта успешно добавлена!'),
                           reply_markup=main_kb)
    await MainStates.first_pg.set()


# удалить карту
# @dp.message_handler(state=number_to_delete)
async def del_card(message: types.Message):
    try:
        number = int(message.text)
        connect = sqlite3.connect('C:\\Users\\1\\Desktop\\bot-for-mom\\database\\cards_db.db')
        cursor = connect.cursor()
        cursor.execute('DELETE FROM cards WHERE card_number=?', (CardStates.card_dict[number],))
        connect.commit()
        cursor.close()
        await message.answer(
            emoji.emojize(f':check_mark_button: Карта {CardStates.card_dict[number]} была успешно удалена!'),
            reply_markup=main_kb)
        await MainStates.first_pg.set()
    except Exception as e:
        print(e)

        await error(message, e)


def db_handlers(dp):
    dp.register_message_handler(del_card, state=CardStates.number_to_delete)
