from aiogram import executor
from create_bot import dp
from handlers import main_handler, requests_handlers, pulya_handler, money_handler, card_handler


async def on_startup(_):
    print('Бот онлайн')

pulya_handler.pulya_handlers(dp)
requests_handlers.requests_handlers(dp)
money_handler.money_handlers(dp)
card_handler.card_handlers(dp)
main_handler.main_handlers(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
