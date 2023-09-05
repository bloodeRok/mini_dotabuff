from aiogram.fsm.state import StatesGroup, State


class AddGameStates(StatesGroup):
    adding_games = State()
    manual_count_input = State()
    user_has_games = State()
