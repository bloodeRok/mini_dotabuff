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
from bot.core.utils.states import BindUserStates, AddGameStates


async def start():
    dp = Dispatcher()
    dp.startup.register(basic_scenario.start_bot)

    # Basic scenarios
    dp.message.register(basic_scenario.get_photo, F.photo)

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
        bind_chat_id_to_user_scenario.where_dota_id,
        F.data.startswith("where_dota_player_id"),
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
        add_games_scenario.add_games_to_user,
        AddGameStates.adding_games
    )
    dp.message.register(
        add_games_scenario.print_count_games,
        AddGameStates.print_count
    )

    # Synchronise scenario
    dp.message.register(
        sychronise_scenario.synchronise_games,
        Command("synchronise")
    )

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
