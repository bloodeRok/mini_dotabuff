from rest_framework import status
from rest_framework.exceptions import APIException


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Entity not found."


class PlayerNotFound(NotFound):
    def __init__(self, nickname: str, user_id: int, game_id: int):
        self.detail = f"Игрок с ником '{nickname}' (id = {user_id})" \
                      f" не был найден в игре (id игры = {game_id})."


class PlayerProfileNotFound(NotFound):
    def __init__(self):
        self.detail = "Я не нашёл профиль с таким ID."


class UserNotFound(NotFound):
    default_detail = "User with this name was not found."


class GameNotFound(NotFound):
    default_detail = "Game with this game_id was not found in db."


class UserGamesNotFound(NotFound):
    default_detail = "User has no recorded games."


class TelegramProfileNotFound(NotFound):
    default_detail = "Telegram profile with this chat_id was not found."
