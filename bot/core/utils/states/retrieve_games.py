from aiogram.fsm.state import StatesGroup, State


class RetrieveGamesStates(StatesGroup):
    filter_games = State()
    validate_filter = State()
    retrieving_games = State()
