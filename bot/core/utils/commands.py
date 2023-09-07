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
            command="add_games",
            description="Добавить игры"
        ),
        BotCommand(
            command="synchronise",
            description="Синхронизировать игры"
        ),
        BotCommand(
            command="photo",
            description="Прислать фото"
        ),
        BotCommand(
            command="retrieve_games",
            description="Вывести игры"
        ),
    ]

    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeDefault()
    )
