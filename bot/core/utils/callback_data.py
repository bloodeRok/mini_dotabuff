from aiogram.filters.callback_data import CallbackData


class RetrieveGames(CallbackData, prefix="filter_games_"):
    filter_by: str
    filter_name: str
