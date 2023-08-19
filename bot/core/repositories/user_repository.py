import aiohttp

from bot.constants.urls import GET_USER_URL, BIND_USER_URL


class UserRepository:

    @staticmethod
    async def get_user(name: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(GET_USER_URL.format(name=name)) as response:
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
