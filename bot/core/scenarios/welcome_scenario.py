from aiogram.types import Message

from bot.core.constants.messages import WELCOME_MESSAGE, HELP_MESSAGE


class WelcomeScenario:
    @staticmethod
    async def send_welcome(message: Message):
        await message.answer(WELCOME_MESSAGE)

    @staticmethod
    async def send_help(message: Message):
        await message.answer(HELP_MESSAGE)