import asyncio

from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.filters import Command

from bot.constants.bot_constants import API_KEY
from bot.core.scenarios import welcome_scenario, bind_scenario, \
    get_stats_scenario, add_game_scenario
from bot.core.handlers import basic
from bot.core.utils.states import BindUserStates, AddGameStates


async def start():
    bot = Bot(token=API_KEY)

    dp = Dispatcher()
    dp.startup.register(basic.start_bot)

    # Get random photo
    dp.message.register(basic.get_photo, F.photo)

    # Welcome scenario
    dp.message.register(
        welcome_scenario.send_welcome,
        Command("start")
    ),

    # Binding scenario
    dp.message.register(
        bind_scenario.start_bind,
        Command("bind")
    ),
    dp.message.register(
        bind_scenario.bind_chat_to_nickname,
        BindUserStates.nickname
    )

    # Get stats
    dp.message.register(
        get_stats_scenario.get_stats,
        Command("get_stats")
    )

    # Add game scenario
    dp.message.register(
        add_game_scenario.start_add_game,
        Command("add_game")
    ),
    dp.message.register(
        add_game_scenario.add_game_to_user,
        AddGameStates.game_id
    )

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
