from rest_framework import status
from rest_framework.exceptions import APIException


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Entity not found."


class PlayerNotFound(NotFound):
    def __init__(self, nickname: str):
        self.detail = f"Игрок с ником '{nickname}'" \
                              f" не был найден в этой игре."


class UserNotFound(NotFound):
    default_detail = "User with this name was not found."


class GameNotFound(NotFound):
    default_detail = "Game with this game_id was not found in db."


class TelegramProfileNotFound(NotFound):
    default_detail = "Telegram profile with this chat_id was not found."
