from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import emoji

choice_1 = KeyboardButton(emoji.emojize('Запрос геолокации :compass:'))

request_kb = ReplyKeyboardMarkup(resize_keyboard=True)
request_kb.add(choice_1)

# inline keyboard

result_yes_button = InlineKeyboardButton('Да', callback_data="send_request")  # все верно, отправить запрос
result_no_button = InlineKeyboardButton('Нет', callback_data='change_request')  # нет, исправить запрос

result_kb = InlineKeyboardMarkup(row_width=2)
result_kb.row(result_yes_button, result_no_button)

# ================

money_yes_button = InlineKeyboardButton('Да', callback_data="send_money")  # отправить деньги
money_no_button = InlineKeyboardButton('Нет', callback_data='not_send_money')  # отказать в деньгах

money_kb = InlineKeyboardMarkup(row_width=2)
money_kb.row(money_yes_button, money_no_button)

# ================

choice_1 = InlineKeyboardButton('Сумму', callback_data="change_amount")  # изменить сумму финансирования
choice_2 = InlineKeyboardButton('Цель', callback_data='change_target')  # изменить цель финансирования

change_request_kb = InlineKeyboardMarkup(row_width=2)
change_request_kb.row(choice_1, choice_2)
