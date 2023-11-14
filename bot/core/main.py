import asyncio

from aiogram import Dispatcher
from aiogram import F
from aiogram.filters import Command

from bot.core.scenarios import (
    bind_chat_id_to_user_scenario,
    get_stats_scenario,
    add_games_scenario,
    basic_scenario,
    sychronise_scenario,
    RetrieveGamesScenario,
    WelcomeScenario
)
from bot.core.utils.bot_init import bot
from bot.core.utils.callback_data import RetrieveGames
from bot.core.utils.states import (
    BindUserStates,
    AddGameStates,
    BasicStates,
    SynchroniseStates,
    RetrieveGamesStates,
)


async def start():
    dp = Dispatcher()
    dp.startup.register(basic_scenario.start_bot)

    retrieve_games_scenario = RetrieveGamesScenario()

    # Basic scenarios
    dp.message.register(basic_scenario.get_photo, F.photo)
    dp.callback_query.register(
        basic_scenario.state_clear,
        F.data.startswith("state_clear")
    )
    dp.message.register(basic_scenario.multiple_def, Command("lol"))
    dp.message.register(basic_scenario.multiple_def, BasicStates.test)
    dp.message.register(basic_scenario.test, Command("test"))

    # Welcome scenario
    dp.message.register(
        WelcomeScenario.send_welcome,
        Command("start")
    ),
    dp.message.register(
        WelcomeScenario.send_help,
        Command("help")
    )

    # Binding scenario
    dp.message.register(
        bind_chat_id_to_user_scenario.start_bind,
        Command("bind")
    ),
    dp.message.register(
        bind_chat_id_to_user_scenario.bind_chat_to_dota_id,
        BindUserStates.dota_id
    )
    dp.callback_query.register(
        bind_chat_id_to_user_scenario.where_dota_id_dotabuff,
        F.data.startswith("where_dota_player_id_dotabuff"),
    )
    dp.callback_query.register(
        bind_chat_id_to_user_scenario.where_dota_id_dota_client,
        F.data.startswith("where_dota_player_id_dota_client"),
    )

    # Get stats scenario
    dp.message.register(
        get_stats_scenario.get_stats,
        Command("get_stats")
    )

    # Add games scenario
    dp.message.register(
        add_games_scenario.start_add_games,
        Command("add_games")
    ),
    dp.message.register(
        sychronise_scenario.user_has_games_in_adding,
        AddGameStates.user_has_games
    )
    dp.message.register(
        add_games_scenario.add_games_to_user,
        AddGameStates.adding_games
    )
    dp.message.register(
        add_games_scenario.manual_count_input,
        AddGameStates.manual_count_input
    )

    # Synchronise scenario
    dp.message.register(
        sychronise_scenario.synchronise_games,
        Command("synchronise")
    )
    dp.message.register(
        add_games_scenario.user_has_no_games_in_synchronise,
        SynchroniseStates.user_has_no_games
    )

    # Retrieve games scenario
    dp.message.register(
        retrieve_games_scenario.start_retrieve_games,
        Command("retrieve_games")
    )
    dp.message.register(
        retrieve_games_scenario.filter_games,
        RetrieveGamesStates.filter_games
    )
    dp.callback_query.register(
        retrieve_games_scenario.add_filter_by_heroes,
        RetrieveGames.filter(F.filter_by == "hero")
    )
    dp.callback_query.register(
        retrieve_games_scenario.add_filter_by_last_days,
        RetrieveGames.filter(F.filter_by == "last_days")
    )
    dp.callback_query.register(
        retrieve_games_scenario.add_filter_by_count,
        RetrieveGames.filter(F.filter_by == "top")
    )
    dp.callback_query.register(
        retrieve_games_scenario.add_filter_by_interval__first,
        RetrieveGames.filter(F.filter_by == "interval")
    )
    dp.message.register(
        retrieve_games_scenario.add_filter_by_interval__second,
        RetrieveGamesStates.second_interval
    )
    dp.callback_query.register(
        retrieve_games_scenario.retrieving_games,
        RetrieveGames.filter(F.filter_by == "over_filterring")
    )
    dp.callback_query.register(
        retrieve_games_scenario.retrieving_games,
        RetrieveGames.filter(F.filter_by == "all_games")
    )
    dp.callback_query.register(
        retrieve_games_scenario.paginating_games,
        RetrieveGamesStates.paginating_games
    )
    dp.callback_query.register(
        retrieve_games_scenario.adding_page,
        F.data.startswith("adding_page"),
    )
    dp.callback_query.register(
        retrieve_games_scenario.subtraction_page,
        F.data.startswith("subtraction_page"),
    )
    dp.callback_query.register(
        retrieve_games_scenario.close_retrieving,
        F.data.startswith("close_retrieving"),
    )

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
