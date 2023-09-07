from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.core.constants.messages import START_RETRIEVE_GAMES_MESSAGE
from bot.core.keyboards import retrieve_games__filter__kb
from bot.core.utils.states import RetrieveGamesStates


async def start_retrieve_games(message: Message, state: FSMContext):
    await message.answer(
        START_RETRIEVE_GAMES_MESSAGE,
        reply_markup=retrieve_games__filter__kb
    )
    await state.set_state(RetrieveGamesStates.retreiving_games)
