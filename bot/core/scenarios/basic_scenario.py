from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery

from bot.core.utils.commands import set_commands


async def get_photo(message: Message, bot: Bot):
    await message.answer(
        "Ну фоточка. Ну здорово. "
        "Ты умеешь отправлять фотографии. Молодец."
    )


async def start_bot(bot: Bot):
    await set_commands(bot=bot)


async def state_clear(state: FSMContext):
    await state.clear()
