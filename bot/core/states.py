from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    start = State()
    add_user = State()
    get_user = State()
