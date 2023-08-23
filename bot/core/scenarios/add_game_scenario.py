from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.core.constants.messages import START_ADD_GAME_MESSAGE
from bot.core.keyboards import add_game__not_found__kb
from bot.core.repositories import UserRepository
from bot.core.utils.states import AddGameStates


async def start_add_game(message: Message, state: FSMContext):
    await message.answer(START_ADD_GAME_MESSAGE)
    await state.set_state(AddGameStates.game_id)


async def add_game_to_user(message: Message, state: FSMContext):
    status, detail = await UserRepository().add_game(
        chat_id=message.chat.id,
        game_id=message.text
    )
    match status:
        case 201:
            await message.answer("Игра успешно добавлена!")

        case 404:
            await message.answer(
                detail + " Почему?",
                reply_markup=add_game__not_found__kb
            )

        case 409:
            await message.answer(
                "Эта игра уже была ранее привязана к этому аккаунту!"
            )

        case 500:
            await message.answer("Что-то пошло не так!")
