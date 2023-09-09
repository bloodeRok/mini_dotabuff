from typing import Any

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.core.constants.bot_constants import HEROES
from bot.core.constants.messages import START_RETRIEVE_GAMES_MESSAGE
from bot.core.keyboards import (
    get_filter_kb,
    retrieve_games__all_heroes__kb, get_invalid_filter_kb, to_admin__kb,
)
from bot.core.repositories import UserRepository
from bot.core.scenarios.helpers.validators import date_is_valid
from bot.core.utils.bot_init import bot
from bot.core.utils.callback_data import RetrieveGames
from bot.core.utils.states import RetrieveGamesStates


class RetrieveGamesScenario:

    @staticmethod
    def __filter_validation(
            filter_value: str | int | list[str],
            last_filter_by: str,
    ):

        match last_filter_by:
            case "hero":
                if filter_value not in HEROES:
                    return False, \
                           "Герой должен быть выбран из выпадающей клавиатуры!"

            case "count" | "last_days":
                try:
                    value = int(filter_value)
                except (ValueError, SyntaxError):
                    return False, \
                           "Это должно быть число!"
                if value < 0:
                    return False, \
                           "Это должно быть положительное число!"

            case "interval":
                for interval in filter_value:
                    if not date_is_valid(interval):
                        return False, \
                               f"Дата ({interval}) задана не в том формате!"

        return True, ""

    @staticmethod
    def __get_filter_str(
            filter_name: str,
            filter_value: str | int | list[str]
    ):

        if filter_name == "hero":
            filter_str = filter_value.replace(" ", "%20")
            return "hero=" + filter_str

        if filter_name == "interval":
            return f"min_date={filter_value[0]}&max_date={filter_value[1]}"

        return f"{filter_name}={filter_value}"

    @staticmethod
    async def start_retrieve_games(message: Message):
        await message.answer(
            START_RETRIEVE_GAMES_MESSAGE,
            reply_markup=get_filter_kb(
                excludes=["over_filterring"]
            )
        )

    async def filter_games(
            self,
            message: Message,
            state: FSMContext
    ):
        data = await state.get_data()

        last_filter_by, last_filter_name = data["last_filter"]["filter_by"], \
                                           data["last_filter"]["filter_name"]

        filter_value = [data["first_interval"], message.text] \
            if last_filter_by == "interval" else message.text

        filter_is_valid, answer = self.__filter_validation(
            filter_value=filter_value,
            last_filter_by=last_filter_by
        )

        if not filter_is_valid:
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
            "value": [data["first_interval"], message.text] \
                if last_filter_by == "interval" else message.text
        }
        await state.update_data(filters=filters)

        str_filters = "\n" + ",\n".join(
            [
                f"{filt['name']} ({filt['value']})" for filt in
                filters.values()
            ]
        )

        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Сейчас выбраны фильтры: "  # TODO interval от до
                 f"{str_filters}\n\n"
                 f"Ещё фильтры?",
            reply_markup=get_filter_kb(
                excludes=list(filters.keys()) + ["all_games"]
            )
        )

    @staticmethod
    async def add_filter_by_heroes(
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

    @staticmethod
    async def add_filter_by_last_days(
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
            text="За сколько последних дней вывести игры?"
        )

        await state.set_state(RetrieveGamesStates.filter_games)

        await call.answer()

    @staticmethod
    async def add_filter_by_count(
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
            text="Какое количество игр вывести?"
        )

        await state.set_state(RetrieveGamesStates.filter_games)

        await call.answer()

    @staticmethod
    async def add_filter_by_interval__first(
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
            text="С какого числа вывести игры?\n\n"
                 "P.S. дата должна быть в формате"
                 " YYYY-MM-DD (год-месяц-число)\n"
                 "Пример: 1999-06-11"
        )

        await state.set_state(RetrieveGamesStates.second_interval)

        await call.answer()

    @staticmethod
    async def add_filter_by_interval__second(
            message: Message,
            state: FSMContext
    ):

        await state.update_data(
            first_interval=message.text
        )

        await bot.send_message(
            chat_id=message.chat.id,
            text="По какое число вывести игры?\n\n"
                 "P.S. дата должна быть в формате"
                 " YYYY-MM-DD (год-месяц-число)\n"
                 "Пример: 1999-06-11"
        )

        await state.set_state(RetrieveGamesStates.filter_games)

    async def retrieving_games(
            self,
            call: CallbackQuery,
            state: FSMContext
    ):

        chat_id = call.message.chat.id

        data = await state.get_data()
        filters_str = None

        filters_dict = data.get("filters")
        if filters_dict:
            filters_str = ".0.?"
            for filter_name, filter_value in filters_dict.items():
                filters_str += self.__get_filter_str(
                    filter_name=filter_name,
                    filter_value=filter_value["value"]
                ) + "&"

            filters_str = filters_str[:-1]

        res_code, data = await UserRepository().retrieve_games(
            chat_id=chat_id,
            filters=filters_str
        )

        match res_code:
            case 200:
                answer = ""
                count = 0
                for game in data:
                    count += 1
                    game_date = game['game_date'][:-1]
                    win = "Победа\n" if game["win"] else "Поражение\n"
                    answer += \
                        f"-------------Игра №{count}-------------\n" \
                        + win \
                        + f"Герой: {game['hero']}\n" \
                          f"Дата игры: {game_date.replace('T', ' ')}\n" \
                          f"Длительность игры: {game['game_duration'][:-1]}\n" \
                          f"KDA: {game['KDA']}\n"
                await bot.send_message(
                    chat_id=chat_id,
                    text=answer
                )

                # case 404:
                #     await message.answer(json["detail"])
                #
                # case 500:
                #     await message.answer(
                #         "Что-то пошло не так!",
                #         reply_markup=to_admin__kb
                #     )
        await state.clear()
