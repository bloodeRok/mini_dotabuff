from aiogram import Bot
from aiogram.types import Message, FSInputFile

from bot.core.utils.commands import set_commands


async def get_photo(message: Message, bot: Bot):
    await message.answer(
        "Ну фоточка. Ну здорово. "
        "Ты умеешь отправлять фотографии. Молодец."
    )


async def start_bot(bot: Bot):
    await set_commands(bot=bot)
