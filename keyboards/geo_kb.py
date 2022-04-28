from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import emoji

geo_yes_button = KeyboardButton(emoji.emojize('Согласиться'), request_location=True)
geo_no_button = KeyboardButton(emoji.emojize('Отказаться'))

geo_kb = ReplyKeyboardMarkup(resize_keyboard=True)
geo_kb.row(geo_yes_button, geo_no_button)