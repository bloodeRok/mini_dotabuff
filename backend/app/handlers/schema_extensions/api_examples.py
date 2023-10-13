from typing import Type

from drf_spectacular.utils import OpenApiExample
from rest_framework.exceptions import APIException

from backend.app import api_exceptions


def build_example(name: str, exception: Type[APIException]) -> OpenApiExample:
    return OpenApiExample(
        name=name,
        value={"detail": exception.default_detail},
        status_codes=[exception.status_code],
        response_only=True
    )


# ------------ 201 ------------

Success = OpenApiExample(
    name="Success",
    value="Success",
    status_codes=[201]
)

# ------------ 404 ------------

PlayerNotFound = build_example(
    name="Player not found in game",
    exception=api_exceptions.PlayerNotFound
)
UserNotFound = build_example(
    name="User not found",
    exception=api_exceptions.UserNotFound
)
GameNotFound = build_example(
    name="Game not found",
    exception=api_exceptions.GameNotFound
)
TelegramProfileNotFound = build_example(
    name="Telegram profile not found",
    exception=api_exceptions.TelegramProfileNotFound
)


# ------------ 406 ------------

InvalidGameId = OpenApiExample(
    name="Open Dota problem",
    value={"detail": "Open Dota not available."},
    status_codes=[406],
    response_only=True
)

InvalidQueryParameter = OpenApiExample(
    name="Invalid query parameter",
    value={"detail": "Unable to parse parameter '1.5' as int."},
    status_codes=[406],
    response_only=True
)

# ------------ 409 ------------

UserConflict = build_example(
    name="User already exists",
    exception=api_exceptions.UserConflict
)

PlayerGameConflict = build_example(
    name="Player already bound to game",
    exception=api_exceptions.PlayerGameConflict
)
