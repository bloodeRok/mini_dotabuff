import asyncio

from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.filters import Command

from bot.core.scenarios import (
    welcome_scenario,
    bind_chat_id_to_user_scenario,
    get_stats_scenario,
    add_games_scenario,
)
from bot.core.handlers import basic
from bot.core.utils.bot_init import bot
from bot.core.utils.states import BindUserStates, AddGameStates



async def start():

    dp = Dispatcher()
    dp.startup.register(basic.start_bot)

    # Basic
    dp.message.register(basic.get_photo, F.photo)

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
        bind_chat_id_to_user_scenario.bind_chat_to_dotabuff_id,
        BindUserStates.dotabuff_id
    )
    dp.callback_query.register(
        bind_chat_id_to_user_scenario.where_dotabuff_id,
        F.data.startswith("where_dotabuff_player_id"),
    )

    # Get stats
    dp.message.register(
        get_stats_scenario.get_stats,
        Command("get_stats")
    )

    # Add games scenario
    dp.message.register(
        add_games_scenario.start_add_games,
        Command("add_game")
    ),
    dp.message.register(
        add_games_scenario.add_games_to_user,
        AddGameStates.adding_games
    )
    dp.message.register(
        add_games_scenario.print_count_games,
        AddGameStates.print_count
    )

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
