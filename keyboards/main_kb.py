from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import emoji

back_button = KeyboardButton(emoji.emojize('Назад :left_arrow:'))

# main buttons

choice_1 = KeyboardButton(emoji.emojize('Запросы :red_question_mark:'))
choice_2 = KeyboardButton(emoji.emojize('Плюпка :black_cat:'))
choice_3 = KeyboardButton(emoji.emojize('Мои карты :credit_card:'))

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(choice_1).add(choice_2).add(choice_3)
