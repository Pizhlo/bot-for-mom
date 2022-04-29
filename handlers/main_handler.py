from aiogram import types
from keyboards.main_kb import main_kb
import sqlite3
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery
from main_files.create_bot import bot
import emoji
from keyboards.pulya_kb import pulya_kb_1
from main_files.common import get_recipient_sender
from handlers.pulya_handler import PulyaStates
from handlers.requests_handlers import RequestStates
from main_files.common import MainStates
from keyboards.main_kb import back_button
import json, string, random
from keyboards.money_kb import cards_kb

allowed_id = [1413785229, 297850814]

phrases_list = [
    "Я вас не понимаю.",
    "Мне не понятна эта команда.",
    "Сформулируйте свой запрос точнее и возвращайтесь ко мне.",
    "Возможно, если бы вы точно знали, чего хотите, то нам обоим бы стало легче, но это неточно.",
    "Эта команда мне неизвестна.",
    "Если у вас возникли проблемы, обратитесь к владельцу бота: @pingwin1234",
    "У меня нет времени на вас. Определитесь, что вам нужно, и тогда пишите сюда.",
    "Вам не нужно писать никаких команд. Просто напишите /start и я отправлю вам клавиатуру со всеми функциями. "
    "А если для вас ограничен доступ - то вообще не нужно ничего писать.",
    "Еще одно такое сообщение и я расскажу своему владельцу.",
    "Со мной шутки плохи, не надо так делать.",
    "Возможно, мне бы удалось вам помочь, если бы вы знали, чего хотите от меня.",
    "Не надо сюда писать ерунду. ",
    "Я не понимаю вашей команды. Проверьте, возможно, вы опечатались.",
    "Ваше сообщение очень важно для меня. Ой, кажется, я научился врать."
]

phrases_list2 = [
    "Я не приемлю обсценную лексику. Пожалуйста, выражайтесь литературно.",
    "Вам не следует материться в переписке со мной.",
    "Такие сообщения оскорбительны для меня.",
    "Извините, я не разговариваю на быдлянском.",
    "А со своими родителями вы тоже так разговариваете?",
    "Можете ещё на холодильник покричать — больше пользы будет.",
    "Свой рот будешь открывать у стоматолога.",
    "Ну давай разберем по частям, тобою написанное )) Складывается впечатление что ты реально контуженный , "
    "обиженный жизнью имбицил )) Могу тебе и в глаза сказать, готов приехать послушать?) Вся та хуйня тобою "
    "написанное это простое пиздабольство , рембо ты комнатный)) от того что ты много написал, жизнь твоя лучше не "
    "станет)) пиздеть не мешки ворочить, много вас таких по весне оттаяло )) Про таких как ты говорят: Мама не "
    "хотела, папа не старался) Вникай в моё послание тебе постарайся проанализировать и сделать выводы для себя) ",
    "Зачем ты это говоришь? Я тоже могу обозвать тебя мудаком. Или вообще всем рассказать, что ты сифилисом "  # This is an optional line
    "переболел. Так что к тебе больше никто не подойдет. Знаешь, что такое клевета? Не отмоешься потом. Так что, "
    "выбирай выражения и следи за своими словами.",
    "Прекрасно владеете матом, голубчик. Биндюжником работали?",
    "У тебя вместо мозгов тормозная жидкость.",
    "В этой группе за гнилой базар платят своей жизнью.",
    "https://sun9-1.userapi.com/sun9-86/impf/lTHW4hSu2us1uWNR_yhI_VQoS0KvNkOuE_qPtw/XKVBOGFCFmQ.jpg?size=1080x660"
    "&quality=96&sign=b18b95c4b31689d88885fd7100507a5a&type=album",
    "Что я слышу! Голос со дна океана тупости. Ты даже не тупой, еще тупее. Клинический имбецил.",
    "Слушай, тебе надо отдохнуть. Может быть тебе съездить куда-нибудь? В нос или в челюсть?"
]


# @dp.message_handler()
async def unknown_msg(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('../cenz_directory/my_cenz.json')))) != set():
        choice = random.choice(phrases_list2)
        await message.answer(choice)
    else:
        choice = random.choice(phrases_list)
        await message.answer(choice)


# @dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    sender, recipient = get_recipient_sender(message.from_user.id)
    if sender in allowed_id:
        await message.answer("Привет!"
                             "\nВыбери, что хочешь сделать",
                             reply_markup=main_kb)
        await MainStates.first_pg.set()
    else:
        await message.answer('Вам запрещено пользоваться данным ботом.',
                             reply_markup=ReplyKeyboardRemove())
        await bot.send_message(297850814, 'Кто-то пытался воспользоваться ботом! '
                                          f'Username = @{message.from_user.username}')


# @dp.message_handler(lambda message: 'Запросы' in message.text)
async def request_cmd(message: types.Message):
    choice_1 = KeyboardButton(emoji.emojize('Запрос геолокации :compass:'))
    request_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    request_kb.add(choice_1)
    if message.from_user.id == 297850814:
        choice_2 = KeyboardButton(emoji.emojize('Запрос на финансирование :dollar_banknote:'))
        request_kb.add(choice_2)
    else:
        pass
    request_kb.add(back_button)
    await RequestStates.first_pg.set()
    await message.answer("Выбери, что хочешь сделать:", reply_markup=request_kb)


# @dp.message_handler(lambda message: 'Плюпка' in message.text)
async def pulya_cmd(message: types.Message):
    await PulyaStates.first_pg.set()
    await message.answer("Выбери, что хочешь сделать:", reply_markup=pulya_kb_1)


add_card = InlineKeyboardButton('Да', callback_data='add_card')
dont_add_card = InlineKeyboardButton('Нет', callback_data='dont_add_card')

add_card_kb = InlineKeyboardMarkup(row_width=2).row(add_card, dont_add_card)


# @dp.message_handler(lambda message: 'Мои карты' in message.text)
async def cards_cmd(message: types.Message):
    connect = sqlite3.connect('C:\\Users\\1\\Desktop\\bot-for-mom\\database\\cards_db.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM cards WHERE user=?', (message.from_user.id,))
    check = cursor.fetchall()

    if not check:
        await message.answer('У вас не добавлено ни одной карты.')
        await message.answer('Хотите добавить карту?', reply_markup=add_card_kb)
    else:
        await message.answer('Вот ваши карты: ', reply_markup=cards_kb)
        i = 1
        for row in check:
            text = f'{i}. Номер карты: {row[1]}\n' \
                   f'Владелец карты: {row[2]}\n' \
                   f'CVV: {row[4]}\n' \
                   f'Срок годности карты: {row[3]}'
            i += 1
            await message.answer(text)


# @dp.callback_query_handler(text='dont_add_card') добавить карту
async def dont_add_card(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'Принято! Что хотите сделать?', reply_markup=main_kb)
    await MainStates.first_pg.set()


def main_handlers(dp):
    dp.register_message_handler(process_start_command, commands=['start'])

    dp.register_message_handler(request_cmd, lambda message: 'Запросы' in message.text, state=MainStates.first_pg)
    dp.register_message_handler(pulya_cmd, lambda message: 'Плюпка' in message.text, state=MainStates.first_pg)
    dp.register_message_handler(cards_cmd, lambda message: 'Мои карты' in message.text, state=MainStates.first_pg)

    dp.register_callback_query_handler(dont_add_card, text='dont_add_card', state="*")

    dp.register_message_handler(unknown_msg, state="*")
