from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.core.keyboards import (
    bind_game__where_dota_id__kb,
    to_admin__kb,
)
from bot.core.repositories import UserRepository
from bot.core.utils.states import BindUserStates
from ..constants.messages import START_BIND_MESSAGE


async def start_bind(message: Message, state: FSMContext):
    await message.answer(
        START_BIND_MESSAGE,
        reply_markup=bind_game__where_dota_id__kb
    )
    await state.set_state(BindUserStates.dota_id)


async def synchronise_games(message: Message, state: FSMContext):

    res_code, json = await UserRepository().bind_user(
        chat_id=message.chat.id,
    )

    match res_code:
        case 201:
            nickname = json["nickname"]
            await message.answer(
                f"Игрок c ником \"{nickname}\" успешно привязан!")

        case 404:
            await message.answer("Я не нашёл профиль с таким ID.")

        case 500:
            await message.answer(
                "Что-то пошло не так!",
                reply_markup=to_admin__kb
            )
    await state.clear()