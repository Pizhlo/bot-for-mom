from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import emoji

# request button


choice_1 = KeyboardButton(emoji.emojize('Запрос геолокации :compass:'))


request_kb = ReplyKeyboardMarkup(resize_keyboard=True)
request_kb.add(choice_1)