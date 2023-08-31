from aiogram.fsm.state import StatesGroup, State


class BindUserStates(StatesGroup):
    dota_id = State()
