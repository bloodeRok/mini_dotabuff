from django.http import HttpResponse, JsonResponse
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request

from core.app.handlers.schema_extensions import api_examples
from core.app.handlers.schema_extensions.api_responses import (
    UserResponse,
    APIResponse,
)
from core.app.serializers.requests import UserCreateRequest, GameBindRequest
from core.app.serializers.responses import UserSerializer
from core.app.services import UserService

@extend_schema_view(
    post=extend_schema(
        tags=["users"],
        operation_id="Bind Game",
        description="Binds game to user supplied parameters.\n"
                    "* Wrote player stats from game in db.\n"
                    "* Auto-creates game if it does not exist.\n",
        request=GameBindRequest,
        responses={
            201: UserResponse().created(),
            404: UserResponse().not_found(
                examples=[
                    api_examples.UserNotFound,
                    api_examples.PlayerNotFound
                ]
            ),
            406: APIResponse.invalid_parameters(
                examples=[
                    api_examples.InvalidGameId
                ]
            ),
            409: UserResponse().conflict(
                examples=[
                    api_examples.PlayerGameConflict
                ]
            ),
        }
    )
)
@api_view(["POST"])
def user_games(
        request: Request,
        name: str
) -> HttpResponse:
    data = GameBindRequest(data=request.data)
    data.is_valid(raise_exception=True)
    data = data.validated_data

    UserService().bind_game(
        game_id=data["game_id"],
        nickname=data["dota_nickname"],
        user_name=name
    )
    return HttpResponse("Success", status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        tags=["users", "retrieve users"],
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
def users_user(
        request: Request,
        name: str
) -> HttpResponse:
    user = UserService().find_by_name(name=name)
    return JsonResponse(UserSerializer(user).data)
