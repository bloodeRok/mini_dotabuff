import aiohttp

from bot.constants.urls import GET_USER_URL, BIND_USER_URL, ADD_GAME_URL


class UserRepository:

    @staticmethod
    async def get_stats(chat_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    GET_USER_URL.format(chat_id=chat_id)
            ) as response:
                return await response.json()

    @staticmethod
    async def bind_user(chat_id: int, nickname: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    BIND_USER_URL,
                    data={
                        "chat_id": chat_id,
                        "nickname": nickname
                    }
            ) as response:
                return response.status

    @staticmethod
    async def add_game(chat_id: int, game_id: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    ADD_GAME_URL.format(chat_id=chat_id),
                    data={
                        "game_id": game_id
                    }
            ) as response:
                return response.status, (await response.json())["detail"]
