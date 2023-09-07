from aiogram.fsm.state import StatesGroup, State


class RetrieveGamesStates(StatesGroup):
    retreiving_games = State()
