from typing import Any

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.core.constants.bot_constants import HEROES
from bot.core.constants.messages import START_RETRIEVE_GAMES_MESSAGE
from bot.core.keyboards import (
    get_filter_kb,
    retrieve_games__all_heroes__kb, get_invalid_filter_kb,
)
from bot.core.utils.bot_init import bot
from bot.core.utils.callback_data import RetrieveGames
from bot.core.utils.states import RetrieveGamesStates


async def start_retrieve_games(message: Message):
    await message.answer(
        START_RETRIEVE_GAMES_MESSAGE,
        reply_markup=get_filter_kb(
            excludes=["over_filterring"]
        )
    )


async def games_no_filter(call: CallbackQuery):
    pass


async def filter_games(
        message: Message,
        state: FSMContext
):
    data = await state.get_data()

    last_filter_by, last_filter_name = data["last_filter"]["filter_by"], \
                                       data["last_filter"]["filter_name"]

    filter_validation, answer = filter_is_valid(
        filter_value=message.text,
        last_filter_by=last_filter_by
    )

    if not filter_validation:
        await message.reply(
            text=answer,
            reply_markup=get_invalid_filter_kb(
                filter_by=last_filter_by,
                filter_name=last_filter_name
            )
        )
        return

    filters = data.get("filters", {})
    filters[last_filter_by] = {
        "name": last_filter_name,
        "value": message.text
    }
    await state.update_data(filters=filters)

    str_filters = "\n" + ",\n".join(
        [
            f"{filt['name']} ({filt['value']})" for filt in filters.values()
        ]
    )
    data_x = await state.get_data()
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Сейчас выбраны фильтры: "
             f"{str_filters}\n"
             f"Ещё фильтры?",
        reply_markup=get_filter_kb(excludes=list(filters.keys()))
    )


async def retrieving_games():
    pass


async def start_add_filter_by_heroes(
        call: CallbackQuery,
        state: FSMContext,
        callback_data: RetrieveGames
):
    await state.update_data(
        last_filter={
            "filter_by": callback_data.filter_by,
            "filter_name": callback_data.filter_name
        }
    )

    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Выбери героя, которого ты хочешь видеть в выборке игр",
        reply_markup=retrieve_games__all_heroes__kb
    )

    await state.set_state(RetrieveGamesStates.filter_games)

    await call.answer()


def filter_is_valid(
        filter_value: [str | int | list[str]],
        last_filter_by: str,
):

    if last_filter_by == "hero":
        if filter_value not in HEROES:
            return False, "Герой должен быть выбран из выпадающей клавиатуры!"

    return True
