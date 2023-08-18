from aiogram.types import Message

from bot.constants.messages import WELCOME_MESSAGE
from bot.core import dp


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: Message):
    await message.reply(WELCOME_MESSAGE)
