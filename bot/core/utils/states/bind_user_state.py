from aiogram.fsm.state import StatesGroup, State


class BindUserStates(StatesGroup):
    nickname = State()
