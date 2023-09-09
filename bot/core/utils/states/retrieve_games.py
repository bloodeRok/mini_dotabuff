from aiogram.fsm.state import StatesGroup, State


class RetrieveGamesStates(StatesGroup):
    second_interval = State()
    filter_games = State()
    validate_filter = State()
    retrieving_games = State()
