from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import emoji
from keyboards.main_kb import back_button

# pulya buttons

forward_button = KeyboardButton(emoji.emojize('Далее :right_arrow:'))

pulya_1 = KeyboardButton(emoji.emojize('Плюпка хочет есть! :cut_of_meat:'))
pulya_2 = KeyboardButton(emoji.emojize('Плюпка покушала! :face_savoring_food:'))
pulya_3 = KeyboardButton(emoji.emojize('Плюпка чихнула! :sneezing_face:'))

pulya_4 = KeyboardButton(emoji.emojize('Плюпка хочет играть! :zany_face:'))
pulya_5 = KeyboardButton(emoji.emojize('Плюпка играет! :squinting_face_with_tongue:'))

pulya_kb_1 = ReplyKeyboardMarkup(resize_keyboard=True)
pulya_kb_1.add(pulya_1).add(pulya_2).add(pulya_3).add(back_button, forward_button)

pulya_kb_2 = ReplyKeyboardMarkup(resize_keyboard=True)
pulya_kb_2.add(pulya_4).add(pulya_5)

pulya_6 = KeyboardButton(emoji.emojize('Спросить, что делает Плюпка :white_question_mark:'))

# inline keyboard

inline_yes_button = InlineKeyboardButton('Да', callback_data="answer") # ответить на вопрос что делает плюпка
inline_no_button = InlineKeyboardButton('Нет', callback_data='dont_answer')  # отказаться

question_inline_kb = InlineKeyboardMarkup(row_width=2)
question_inline_kb.row(inline_yes_button, inline_no_button)