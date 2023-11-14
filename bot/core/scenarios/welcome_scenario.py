from aiogram.types import Message

from bot.core.constants.messages import WELCOME_MESSAGE, HELP_MESSAGE
from bot.core.keyboards import to_admin__kb


class WelcomeScenario:
    @staticmethod
    async def send_welcome(message: Message):
        await message.answer(
            WELCOME_MESSAGE,
            reply_markup=to_admin__kb
        )

    @staticmethod
    async def send_help(message: Message):
        await message.answer(HELP_MESSAGE)
