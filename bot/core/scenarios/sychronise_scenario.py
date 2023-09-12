from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.core.keyboards import (
    to_admin__kb, synchronise__from_synchronise_to_add__kb,
)
from bot.core.repositories import UserRepository
# from .add_games_scenario import start_add_games
from ..constants.sticker_constants import DOWNLOAD
from ..utils.bot_init import bot
from ..utils.states import SynchroniseStates


async def synchronise_games(message: Message, state: FSMContext):
    chat_id = message.chat.id

    download_messages = [
        await bot.send_message(
            chat_id=chat_id,
            text="Идёт процесс синхронизации... Подождите."
        ),
        await bot.send_sticker(
            chat_id=chat_id,
            sticker=DOWNLOAD
        )
    ]

    res_code, detail = await UserRepository().synchronise_games(
        chat_id=chat_id,
    )

    for message in download_messages:
        await message.delete()

    match res_code:
        case 201:
            await message.answer(
                f"Игры успешно синхронизованы!"
            )
            await state.clear()

        case 404:
            await bot.send_message(
                chat_id=message.chat.id,
                text="У тебя ещё нет добавленных игр."
                     " Добавить игры?",
                reply_markup=synchronise__from_synchronise_to_add__kb
            )
            await state.set_state(SynchroniseStates.user_has_no_games)

        case 500:
            await message.answer(
                "Что-то пошло не так!",
                reply_markup=to_admin__kb
            )
            await state.clear()


async def user_has_games_in_adding(message: Message, state: FSMContext):
    if message.text == "Да":
        await synchronise_games(message=message, state=state)
        return
    await bot.send_message(chat_id=message.chat.id, text="Ну ладно...")
    await state.clear()
