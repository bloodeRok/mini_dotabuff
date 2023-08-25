from aiogram.fsm.state import StatesGroup, State


class BindUserStates(StatesGroup):
    dotabuff_id = State()
