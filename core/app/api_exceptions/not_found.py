from typing import Optional

from rest_framework import status
from rest_framework.exceptions import APIException


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Entity not found."


class PlayerNotFound(NotFound):
    def __init__(
            self,
            dota_id: int,
            nickname: Optional[str] = None,
            game_id: Optional[int] = None
    ):
        self.detail = "Игрок {0}(id игрока = {1}) не был найден{2}.".format(
            f"с ником '{nickname}' " if nickname else "",
            dota_id,
            f" в игре (id игры = {game_id})" if game_id else ""
        )


class PlayerProfileNotFound(NotFound):
    def __init__(self):
        self.detail = "Я не нашёл профиль с таким ID."


class UserNotFound(NotFound):
    default_detail = "User with this name was not found."


class GameNotFound(NotFound):
    default_detail = "Game with this game ID was not found in db."


class UserGamesNotFound(NotFound):
    default_detail = "User has no recorded games."


class TelegramProfileNotFound(NotFound):
    default_detail = "Telegram profile with this chat ID was not found."
