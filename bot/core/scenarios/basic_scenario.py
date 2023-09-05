from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery

from bot.core.utils.bot_init import bot
from bot.core.utils.commands import set_commands
from bot.core.utils.states import BasicStates


async def get_photo(message: Message, state: FSMContext):
    await message.answer(
        "Ну фоточка. Ну здорово. "
        "Ты умеешь отправлять фотографии. Молодец."
    )


async def test(message: Message, state: FSMContext):
    await message.answer("Я тесьлвая затычка!")
    await state.set_state(BasicStates.test)


async def start_bot(bot: Bot):
    await set_commands(bot=bot)


async def state_clear(state: FSMContext):
    await state.clear()


async def multiple_def(message: Message, state: FSMContext):
    await message.answer(text="LOL")

