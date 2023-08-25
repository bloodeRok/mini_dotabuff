from aiogram.fsm.state import StatesGroup, State


class AddGameStates(StatesGroup):
    adding_games = State()
    print_count = State()
