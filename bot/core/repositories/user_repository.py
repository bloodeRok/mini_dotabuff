import aiohttp
from aiohttp import ContentTypeError

from bot.core.constants.urls import GET_USER_URL, BIND_USER_URL, ADD_GAMES_URL


class UserRepository:

    @staticmethod
    async def get_stats(chat_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    GET_USER_URL.format(chat_id=chat_id)
            ) as response:
                return await response.json()

    @staticmethod
    async def bind_user(chat_id: int, dotabuff_user_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    BIND_USER_URL,
                    data={
                        "chat_id": chat_id,
                        "dotabuff_user_id": dotabuff_user_id
                    }
            ) as response:
                try:
                    json = await response.json()
                except ContentTypeError:
                    json = None
                return response.status, json

    @staticmethod
    async def add_games(chat_id: int, count: int):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    ADD_GAMES_URL.format(chat_id=chat_id),
                    data={
                        "count": count
                    }
            ) as response:
                detail = None
                status_code = response.status
                if status_code not in [201, 406, 500]:
                    detail = (await response.json())["detail"]
                return status_code, detail
