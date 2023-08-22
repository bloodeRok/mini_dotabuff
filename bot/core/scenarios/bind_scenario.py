from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.constants.messages import START_BIND_MESSAGE
from bot.constants.sticker_constants import TWO_MONKEYS
from bot.core.repositories import UserRepository
from bot.core.utils.states import BindUserStates


async def start_bind(message: Message, state: FSMContext):
    await message.answer(START_BIND_MESSAGE)
    await state.set_state(BindUserStates.nickname)


async def bind_chat_to_nickname(message: Message, state: FSMContext):
    res_code = await UserRepository().bind_user(
        chat_id=message.chat.id,
        nickname=message.text
    )
    await message.answer(
        "Игрок успешно привязан!" if res_code == 204
        else "Что-то пошло не так!"
    )
    await state.clear()
