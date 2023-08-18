from aiogram import Bot, Dispatcher

from bot.constants.bot_constants import API_KEY

bot = Bot(token=API_KEY)
dp = Dispatcher(bot=bot)
