from django.http import HttpResponse, JsonResponse
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from core.app.handlers.schema_extensions import api_examples
from core.app.handlers.schema_extensions.api_responses import (
    TelegramProfileResponse, UserResponse, APIResponse,
)
from core.app.serializers.requests import TelegramProfileCreateRequest, \
    GameBindRequest
from core.app.serializers.responses import UserSerializer
from core.app.services import TelegramProfileService, UserService


@extend_schema_view(
    post=extend_schema(
        tags=["telegram profiles", "create"],
        operation_id="Create Telegram Profile",
        description="Creates Telegram Profile with supplied parameters.\n"
                    "* Creates user if it was not found by dotabuff_id.",
        request=TelegramProfileCreateRequest,
        responses={
            204: TelegramProfileResponse().updated()
        }
    )
)
@api_view(["POST"])
def tgprofiles(
        request: Request
) -> HttpResponse:
    data = TelegramProfileCreateRequest(data=request.data)
    data.is_valid(raise_exception=True)
    data = data.validated_data

    nickname = TelegramProfileService().get_or_create(
        chat_id=data["chat_id"],
        dotabuff_user_id=data["dotabuff_user_id"]
    )
    return Response(
        data={"nickname": nickname},
        status=status.HTTP_201_CREATED
    )


@extend_schema_view(
    get=extend_schema(
        tags=["users", "retrieve users", "telegram profiles"],
        operation_id="Retrieve User",
        description="Retrieves requested user.",
        responses={
            200: UserResponse().single(),
            404: UserResponse().not_found(
                examples=[
                    api_examples.UserNotFound
                ]
            )
        }
    )
)
@api_view(["GET"])
def tgprofiles_users_user(
        request: Request,
        chat_id: int,
) -> HttpResponse:
    user = UserService().find_by_chat_id(chat_id=chat_id)
    return JsonResponse(UserSerializer(user).data)


@extend_schema_view(
    post=extend_schema(
        tags=["telegram profiles", "games"],
        operation_id="Synchronise Games",
        description="Synchronises requested count of games to user.\n"
                    "* Wrote player stats from game in db.\n"
                    "* Auto-creates game if it does not exist.\n",
        request=GameBindRequest,
        responses={
            201: TelegramProfileResponse().created(),
            404: TelegramProfileResponse().not_found(
                examples=[
                    api_examples.TelegramProfileNotFound,
                    api_examples.PlayerNotFound
                ]
            ),
            406: APIResponse.invalid_parameters(
                examples=[
                    api_examples.InvalidGameId
                ]
            ),
            409: TelegramProfileResponse().conflict(
                examples=[
                    api_examples.PlayerGameConflict
                ]
            ),
        }
    )
)
@api_view(["POST"])
def tgprofile_games(
        request: Request,
        chat_id: int
) -> HttpResponse:
    data = GameBindRequest(data=request.data)
    data.is_valid(raise_exception=True)
    data = data.validated_data

    TelegramProfileService().bind_game(
        game_count=data["game_count"],
        chat_id=chat_id
    )
    return HttpResponse("Success", status=status.HTTP_201_CREATED)
