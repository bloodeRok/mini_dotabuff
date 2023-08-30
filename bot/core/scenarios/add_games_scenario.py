from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.core.constants.messages import START_ADD_GAME_MESSAGE
from bot.core.constants.sticker_constants import DOWNLOAD
from bot.core.keyboards import add_game__count__kb, to_admin__kb
from bot.core.repositories import UserRepository
from bot.core.utils.bot_init import bot
from bot.core.utils.states import AddGameStates


async def start_add_games(message: Message, state: FSMContext):
    await message.answer(
        START_ADD_GAME_MESSAGE,
        reply_markup=add_game__count__kb
    )
    await state.set_state(AddGameStates.adding_games)


async def add_games_to_user(message: Message, state: FSMContext):
    a = 5
    user_answer = message.text
    if user_answer == "Сам введу":
        await state.set_state(AddGameStates.print_count)
        return

    chat_id = message.chat.id
    count = int(message.text)

    if count > 50:
        await bot.send_message(
            text="Максимум первоначально записанных игр: 50."
                 " Я установил это значение на 50.",
            chat_id=chat_id
        )

    msg = await bot.send_sticker(
        chat_id=message.chat.id,
        sticker=DOWNLOAD
    )

    status, detail = await UserRepository().add_games(
        chat_id=message.chat.id,
        count=count
    )

    await msg.delete()

    await print_result(message=message, status=status, detail=detail)


async def print_count_games(message: Message, state: FSMContext):
    try:
        count = int(message.text)
    except ValueError:
        await message.reply("Количество игр должно иметь только цифры!")
        return

    await bot.send_sticker(
        chat_id=message.chat.id,
        sticker=DOWNLOAD
    )

    status, detail = await UserRepository().add_games(
        chat_id=message.chat.id,
        count=count
    )

    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    await print_result(message=message, status=status, detail=detail)

    await state.set_state(AddGameStates.adding_games)


async def print_result(message: Message, status: int, detail: Optional[str]):
    match status:
        case 201:
            await message.answer("Игры успешно добавлены!")

        case 404:
            await message.answer(detail)

        case 406:
            await message.answer("Они думают, что мы дудосеры :(")

        case 409:
            await message.answer(
                "У тебя уже есть добавленные игры."
                " Синхронизовать твои игры?",
                # TODO reply_markup=
            )

        case 500:
            await message.answer(
                "Что-то пошло не так!",
                reply_markup=to_admin__kb
            )
