from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import emoji


# ================

button_1 = KeyboardButton(emoji.emojize('Добавить карту :credit_card:'))
button_2 = KeyboardButton(emoji.emojize('Удалить карту :cross_mark:'))
cards_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(button_1, button_2)