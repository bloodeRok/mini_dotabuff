from aiogram.types import Message

from bot.constants.messages import WELCOME_MESSAGE
from bot.constants.sticker_constants import TWO_MONKEYS


async def send_welcome(message: Message):
    await message.answer(WELCOME_MESSAGE)
