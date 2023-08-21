from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.constants.messages import START_ADD_GAME_MESSAGE
from bot.core.keyboards import not_found_add_game_kb
from bot.core.repositories import UserRepository
from bot.core.utils.states import AddGameStates

@dp
async def start_add_game(message: Message, state: FSMContext):
    await message.answer(START_ADD_GAME_MESSAGE)
    await state.set_state(AddGameStates.game_id)


async def add_game_to_user(message: Message, state: FSMContext):
    res_code = await UserRepository().add_game(
        chat_id=message.chat.id,
        game_id=message.text
    )
    match res_code:
        case 201:
            await message.answer("Игра успешно добавлена!")

        case 404:
            await message.answer(
                "Твой ник не было найден в этой игре! Почему?",
                reply_markup=not_found_add_game_kb
            )

        case 409:
            await message.answer(
                "Эта игра уже была ранее привязана к этому аккаунту!"
            )

        case 500:
            await message.answer("Что-то пошло не так!")
