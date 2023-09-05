from aiogram.fsm.state import StatesGroup, State


class SynchroniseStates(StatesGroup):
    user_has_no_games = State()
