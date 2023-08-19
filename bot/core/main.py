import asyncio

from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.filters import Command

from bot.constants.bot_constants import API_KEY
from bot.core.scenarios import welcome_scenario, bind_scenario
from bot.core.handlers import basic
from bot.core.utils.states import WelcomeStates


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
        WelcomeStates.nickname
    )

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
