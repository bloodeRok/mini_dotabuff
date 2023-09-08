from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.constants.bot_constants import HEROES
from bot.core.utils.callback_data import RetrieveGames

retrieve_games__all_heroes__buttons = [
    [
        KeyboardButton(
            text=hero
        )
    ]
    for hero in HEROES
]

retrieve_games__all_heroes__kb = ReplyKeyboardMarkup(
    keyboard=retrieve_games__all_heroes__buttons,
    resize_keyboard=True,
    one_time_keyboard=True
)


# filter buttons
def get_filter_kb(
        excludes: list[str] = None
):
    builder = InlineKeyboardBuilder()
    if "last_days" not in excludes:
        builder.button(
            text="За последние дни",
            callback_data=RetrieveGames(
                filter_by="last_days",
                filter_name="по последним дням"
            )
        )

    if "hero" not in excludes:
        builder.button(
            text="По герою",
            callback_data=RetrieveGames(
                filter_by="hero",
                filter_name="по герою"
            )
        )
    if "count" not in excludes:
        builder.button(
            text="По количеству",
            callback_data=RetrieveGames(
                filter_by="count",
                filter_name="по количеству"
            )
        )
    if "interval" not in excludes:
        builder.button(
            text="Интервал дат (от ... до)",
            callback_data=RetrieveGames(
                filter_by="interval",
                filter_name="по интервалу дат"
            )
        )
    if "all_games" not in excludes:
        builder.button(
            text="Просто все игры",
            callback_data="no_filter"
        )
    if "over_filterring" not in excludes:
        builder.button(
            text="Это все фильтры, покажи игры",
            callback_data="no_filter"
        )

    builder.adjust(2, 1, 1, 1)
    return builder.as_markup()


def get_invalid_filter_kb(
        filter_by: str,
        filter_name: str
):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Ввести ещё раз",
        callback_data=RetrieveGames(
            filter_by=filter_by,
            filter_name=filter_name
        )
    )
    return builder.as_markup()
