import aiohttp

from bot.core.constants.urls import RETRIEVE_HEROES_URL


class HeroRepository:

    @staticmethod
    async def get_heroes() -> list[str]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=RETRIEVE_HEROES_URL
            ) as response:
                return [hero["name"] for hero in await response.json()]
