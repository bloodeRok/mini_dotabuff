from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description="Начало работы"
        ),
        BotCommand(
            command="help",
            description="Помощь"
        ),
        BotCommand(
            command="bind",
            description="Привязать чат к нику в доте"
        ),
        BotCommand(
            command="get_stats",
            description="Получить статистику"
        ),
        BotCommand(
            command="add_game",
            description="Добавить игру"
        ),
        BotCommand(
            command="photo",
            description="Прислать фото"
        ),

    ]

    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeDefault()
    )
