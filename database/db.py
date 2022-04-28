import sqlite3
from main_files.create_bot import bot


# добавить новую карту
async def add_new_card(user_id, card_number, cardholder, date, cvv):
    arr = (user_id, card_number, cardholder, date, cvv)
    connect = sqlite3.connect('C:\\Users\\pizhlo21\\Desktop\\Folder\\python\\bot_for_mom\\database\\cards_db.db')
    cursor = connect.cursor()
    cursor.executemany('INSERT INTO cards VALUES(?, ?, ?, ?, ?)', (user_id, card_number, cardholder, date, cvv))
    connect.commit()
    cursor.close()
    await check(user_id)


async def check(user_id):
    connect = sqlite3.connect('C:\\Users\\pizhlo21\\Desktop\\Folder\\python\\bot_for_mom\\database\\cards_db.db')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM cards")
    rows = cursor.fetchall()

    await bot.send_message(user_id, 'Ваша карта успешно добавлена! Вот данные вашей карты: ')

    for row in rows:
        print(row)
        await bot.send_message(user_id, row)

    cursor.close()
