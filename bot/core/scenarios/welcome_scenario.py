from aiogram.types import Message

from bot.core.constants.messages import WELCOME_MESSAGE


async def send_welcome(message: Message):
    await message.answer(WELCOME_MESSAGE)
