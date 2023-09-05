from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.core.constants.messages import START_ADD_GAME_MESSAGE
from bot.core.constants.sticker_constants import DOWNLOAD
from bot.core.keyboards import add_game__count__kb, to_admin__kb
from bot.core.keyboards.add_games_keyboards import (
    add_games__from_add_to_synchronise__kb,
)
from bot.core.repositories import UserRepository
from .sychronise_scenario import synchronise_games
from bot.core.utils.bot_init import bot
from bot.core.utils.states import AddGameStates


async def start_add_games(message: Message, state: FSMContext):
    await message.answer(
        START_ADD_GAME_MESSAGE,
        reply_markup=add_game__count__kb
    )
    await state.set_state(AddGameStates.adding_games)


async def add_games_to_user(message: Message, state: FSMContext):
    user_answer = message.text
    if user_answer == "Сам введу":
        await bot.send_message(
            chat_id=message.chat.id,
            text="Введи число игр, которое ты хочешь добавить"
        )
        await state.set_state(AddGameStates.manual_count_input)
        return

    await adding_games_to_user(
        message=message,
        count=int(message.text),
        state=state
    )


async def manual_count_input(message: Message, state: FSMContext):
    chat_id = message.chat.id

    try:
        count = int(message.text)
    except ValueError:
        await message.reply("Количество игр должно иметь только цифры!")
        return

    if count > 50:
        await bot.send_message(
            text="Максимум первоначально записанных игр: 50."
                 " Я установил это значение на 50.",
            chat_id=chat_id
        )
        count = 50

    await adding_games_to_user(
        message=message,
        count=count,
        state=state
    )


async def adding_games_to_user(
        message: Message,
        count: int,
        state: FSMContext
):
    chat_id = message.chat.id
    wait_time = int(count * 0.6)

    download_messages = [
        await bot.send_message(
            chat_id=chat_id,
            text="Идёт процесс добавления... Подождите\n"
                 f"Примерное время ожидания: {wait_time} сек"
        ),
        await bot.send_sticker(
            chat_id=chat_id,
            sticker=DOWNLOAD
        )
    ]

    status, detail = await UserRepository().add_games(
        chat_id=chat_id,
        count=count
    )

    for message in download_messages:
        await message.delete()

    await print_result(
        message=message,
        status=status,
        detail=detail,
        state=state
    )


async def print_result(
        message: Message,
        status: int,
        detail: Optional[str],
        state: FSMContext
):
    match status:
        case 201:
            await message.answer("Игры успешно добавлены!")
            await state.clear()

        case 404:
            await message.answer(detail)
            await state.clear()

        case 406:
            await message.answer("Они думают, что мы дудосеры :(")
            await state.clear()

        case 409:
            await bot.send_message(
                chat_id=message.chat.id,
                text="У тебя уже есть добавленные игры."
                " Синхронизовать твои игры?",
                reply_markup=add_games__from_add_to_synchronise__kb
            )
            await state.set_state(AddGameStates.user_has_games)

        case 500:
            await message.answer(
                "Что-то пошло не так!",
                reply_markup=to_admin__kb
            )
            await state.clear()


async def user_has_games(message: Message, state: FSMContext):
    if message.text == "Да":
        await synchronise_games(message=message, state=state)
        return
    await bot.send_message(chat_id=message.chat.id, text="Ну ладно...")
    await state.clear()
