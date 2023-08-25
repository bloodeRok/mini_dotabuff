from aiogram.types import Message

from bot.core.repositories import UserRepository


async def get_stats(message: Message):
    res = await UserRepository().get_stats(chat_id=message.chat.id)
    await message.reply(
        f"name : {res.get('name')}\n"
        f"matches_recorded : {res.get('matches_recorded')}\n"
        f"win_rate : {res.get('win_rate')}\n"
        f"favorite_hero : {res.get('favorite_hero')}\n"
        f"avg_gpm : {res.get('avg_gpm')}\n"
        f"avg_xpm : {res.get('avg_xpm')}\n"
        f"avg_kda : {res.get('avg_kda')}\n"
    )
