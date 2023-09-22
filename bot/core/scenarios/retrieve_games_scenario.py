from math import ceil
from typing import Any

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.core.constants.messages import START_RETRIEVE_GAMES_MESSAGE
from bot.core.keyboards import RetrieveGamesKeyboards, to_admin__kb
from bot.core.repositories import UserRepository, HeroRepository
from bot.core.scenarios.helpers.validators import date_is_valid
from bot.core.utils.bot_init import bot
from bot.core.utils.callback_data import RetrieveGames
from bot.core.utils.states import RetrieveGamesStates


class FilterValidationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class RetrieveGamesScenario:
    heroes = []

    def __filter_validation(
            self,
            filter_value: str | int | list[str],
            last_filter_by: str,
    ):

        match last_filter_by:
            case "hero":
                if filter_value not in self.heroes:
                    raise FilterValidationError(
                        "Герой должен быть выбран из выпадающей клавиатуры!"
                    )

            case "top" | "last_days":
                try:
                    value = int(filter_value)
                except (ValueError, SyntaxError):
                    raise FilterValidationError(
                        "Это должно быть число!"
                    )
                if value < 0:
                    raise FilterValidationError(
                        "Это должно быть положительное число!"
                    )

            case "interval":
                for interval in filter_value:
                    if not date_is_valid(interval):
                        raise FilterValidationError(
                            f"Дата ({interval}) задана не в том формате!"
                        )

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

    async def __get_games(self, chat_id: int, filters_dict: dict[str, Any]):

        filters_str = None

        if filters_dict:
            filters_str = "?"
            for filter_name, filter_value in filters_dict.items():
                filters_str += self.__get_filter_str(
                    filter_name=filter_name,
                    filter_value=filter_value["value"]
                ) + "&"

            filters_str = filters_str[:-1]

        return await UserRepository().retrieve_games(
            chat_id=chat_id,
            filters=filters_str
        )

    @staticmethod
    def __get_game_str(
            count: int,
            win: str,
            hero: str,
            game_date: str,
            game_duration: str,
            kda: str
    ) -> str:
        return f"\n-------------Игра №{count}-------------\n" \
               + win \
               + f"Герой: {hero}\n" \
                 f"Дата игры: {game_date.replace('T', ' ')}\n" \
                 f"Длительность игры: {game_duration}\n" \
                 f"KDA: {kda}\n"

    async def __get_games_answer(
            self,
            games: list[dict[str, str | bool]]
    ) -> dict[int, str]:

        games_dict = {}
        for game_number in range(ceil(len(games) / 20)):
            games_dict[game_number + 1] = \
                games[game_number * 20: (game_number + 1) * 20]
        for page in games_dict:
            page_games = ""
            count = (page - 1) * 20
            for game in games_dict[page]:
                count += 1
                page_games += self.__get_game_str(
                    count=count,
                    win="Победа\n" if game["win"] else "Поражение\n",
                    hero=game["hero"],
                    game_date=game['game_date'][:-1].replace("T", " "),
                    game_duration=game["game_duration"][:-1],
                    kda=game["KDA"]
                )
            games_dict[page] = page_games + f"\nТекущая страница: " \
                                            f"{page} из {len(games_dict)}"
        return games_dict

    @staticmethod
    async def start_retrieve_games(message: Message):
        await message.answer(
            START_RETRIEVE_GAMES_MESSAGE,
            reply_markup=RetrieveGamesKeyboards().get_filter_kb(
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

        try:
            self.__filter_validation(
                filter_value=filter_value,
                last_filter_by=last_filter_by
            )
        except FilterValidationError as e:
            await message.reply(
                text=str(e),
                reply_markup=RetrieveGamesKeyboards().get_invalid_filter_kb(
                    filter_by=last_filter_by,
                    filter_name=last_filter_name
                )
            )
            return

        filters = data.get("filters", {})
        filters[last_filter_by] = {
            "name": last_filter_name,
            "value": filter_value
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
            reply_markup=RetrieveGamesKeyboards().get_filter_kb(
                excludes=list(filters.keys()) + ["all_games"]
            )
        )

    async def add_filter_by_heroes(
            self,
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

        heroes = await HeroRepository.get_heroes()
        self.heroes = heroes

        await bot.send_message(
            chat_id=call.message.chat.id,
            text="Выбери героя, которого ты хочешь видеть в выборке игр",
            reply_markup=RetrieveGamesKeyboards().get_hero_kb(heroes=heroes)
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
        res_code, json = await self.__get_games(
            chat_id=chat_id,
            filters_dict=data.get("filters")
        )

        match res_code:
            case 200:
                if not json:
                    await bot.send_message(
                        chat_id=chat_id,
                        text="Я не нашёл игр с таким фильтром :("
                    )
                    await call.answer()
                    await state.clear()
                    return

                games_dict = await self.__get_games_answer(games=json)
                if len(games_dict) > 1:
                    await state.update_data(
                        current_page=1,
                        games_dict=games_dict
                    )
                    await self.paginating_games(chat_id=chat_id, state=state)
                    return

                await bot.send_message(
                    chat_id=chat_id,
                    text=games_dict[1]
                )

            case 404:
                await call.message.answer(json["detail"])

            case 500:
                await call.message.answer(
                    "Что-то пошло не так!",
                    reply_markup=to_admin__kb
                )

        await call.answer()
        await state.clear()

    @staticmethod
    async def paginating_games(state: FSMContext, chat_id: int):
        data = await state.get_data()
        current_page = data["current_page"]
        games_dict = data["games_dict"]

        await bot.send_message(
            chat_id=chat_id,
            text=games_dict[current_page],
            reply_markup=RetrieveGamesKeyboards.get_paginate_kb(
                games=games_dict,
                page=current_page
            )
        )

    async def adding_page(
            self,
            call: CallbackQuery,
            state: FSMContext
    ):
        data = await state.get_data()
        await state.update_data(current_page=data["current_page"] + 1)
        await call.answer()
        await self.paginating_games(chat_id=call.message.chat.id, state=state)

    async def subtraction_page(
            self,
            call: CallbackQuery,
            state: FSMContext
    ):
        data = await state.get_data()
        await state.update_data(current_page=data["current_page"] - 1)
        await call.answer()
        await self.paginating_games(chat_id=call.message.chat.id, state=state)

    @staticmethod
    async def close_retrieving(
            call: CallbackQuery,
            state: FSMContext
    ):
        await bot.send_message(
            chat_id=call.message.chat.id,
            text="Ну хорошо"
        )
        await state.clear()
        await call.answer()
