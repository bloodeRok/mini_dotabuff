from aiogram.fsm.state import StatesGroup, State


class AddGameStates(StatesGroup):
    game_id = State()
