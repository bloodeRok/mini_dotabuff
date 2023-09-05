import asyncio

from aiogram import Dispatcher
from aiogram import F
from aiogram.filters import Command

from bot.core.scenarios import (
    welcome_scenario,
    bind_chat_id_to_user_scenario,
    get_stats_scenario,
    add_games_scenario,
    basic_scenario,
    sychronise_scenario
)
from bot.core.utils.bot_init import bot
from bot.core.utils.states import BindUserStates, AddGameStates, BasicStates, \
    SynchroniseStates


async def start():
    dp = Dispatcher()
    dp.startup.register(basic_scenario.start_bot)

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
        welcome_scenario.send_welcome,
        Command("start")
    ),

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

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
