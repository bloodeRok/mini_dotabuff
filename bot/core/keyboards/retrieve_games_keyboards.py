from enum import Enum
from typing import Optional

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot.core.constants.bot_constants import HEROES
from bot.core.utils.callback_data import RetrieveGames

from .helpers.enums import RetrieveGamesButtons


class RetrieveGamesKeyboards:

    @staticmethod
    def __filter_button_builder(
            builder: InlineKeyboardBuilder,
            filter_enum: Optional[Enum] = None
    ) -> None:
        """
        TODO docstring
        """

        builder.button(
            text=filter_enum.value.capitalize(),
            callback_data=RetrieveGames(
                filter_by=filter_enum.name,
                filter_name=filter_enum.value
            )
        )

    # heroes buttons
    @staticmethod
    def get_hero_kb(heroes: list[str] = None):
        builder = ReplyKeyboardBuilder()

        for hero in heroes:
            builder.button(text=hero)

        builder.adjust(*[1] * len(heroes))
        return builder.as_markup()

    # filter buttons
    def get_filter_kb(
            self,
            excludes: list[str] = None
    ):
        builder = InlineKeyboardBuilder()

        enum_buttons = [enum for enum in RetrieveGamesButtons]

        for enum_button in enum_buttons:
            if enum_button.name not in excludes:
                self.__filter_button_builder(
                    builder=builder,
                    filter_enum=enum_button
                )

        builder.adjust(*[1] * len(enum_buttons))
        return builder.as_markup()

    @staticmethod
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
