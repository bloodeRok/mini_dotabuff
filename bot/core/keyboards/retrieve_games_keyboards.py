from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Inlin
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.utils.callback_data import RetrieveGames

# filter buttons
def get_filter_kb():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="По дате",
        callback_data=RetrieveGames(filter="date")
    )
    builder.button(
        text="По герою",
        callback_data=RetrieveGames(filter="hero")
    )
    builder.button(
        text="По количеству",
        callback_data=RetrieveGames(filter="count")
    )
    builder.button(
        text="Просто все игры",
        callback_data=RetrieveGames(filter="no")
    )

    builder.adjust(2)
    return builder.as_markup()
