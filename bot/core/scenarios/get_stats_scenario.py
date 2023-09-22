from aiogram.types import Message

from bot.core.repositories import UserRepository


async def get_stats(message: Message):
    res = await UserRepository().get_stats(chat_id=message.chat.id)
    await message.answer(
        f"Ник в доте: {res.get('name')}\n"
        f"Записанных матчей: {res.get('matches_recorded')}\n"
        f"Процент побед: {res.get('win_rate')}\n"
        f"Любимый герой: {res.get('favorite_hero')}\n"
        f"\nСредние показатели: \n"
        f"Золота в минуту: {res.get('avg_gpm')}\n"
        f"Опыта в минуту: {res.get('avg_xpm')}\n"
        f"KDA: {res.get('avg_kda')}\n"
    )
