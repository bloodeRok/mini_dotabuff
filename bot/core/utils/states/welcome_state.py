from aiogram.fsm.state import StatesGroup, State


class WelcomeStates(StatesGroup):
    nickname = State()
