import aiohttp

from bot.core.constants.urls import RETRIEVE_HEROES_URL


class UserRepository:

    @staticmethod
    async def get_stats(chat_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=RETRIEVE_HEROES_URL
            ) as response:
                return await response.json()