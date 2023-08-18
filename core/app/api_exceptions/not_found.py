from rest_framework import status
from rest_framework.exceptions import APIException


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Entity not found."


class PlayerNotFound(NotFound):
    default_detail = "Player with that nickname was not found in this game."


class UserNotFound(NotFound):
    default_detail = "User with this name was not found."
