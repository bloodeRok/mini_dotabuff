from django.http import HttpResponse, JsonResponse
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .helpers.query_parameters_helper import (
    TopQueryParameter,
    MinDateQueryParameter,
    MaxDateQueryParameter,
    LastDaysQueryParameter,
    HeroQueryParameter,
    WinQueryParameter, parse_query_parameter
)

from core.app.handlers.schema_extensions import api_examples
from core.app.handlers.schema_extensions.api_responses import (
    TelegramProfileResponse,
    UserResponse,
    APIResponse, PlayerGameResponse,

)
from core.app.serializers.requests import (
    TelegramProfileCreateRequest,
    GamesAddRequest,
)
from core.app.serializers.responses import UserSerializer, PlayerGameSerializer
from core.app.services import TelegramProfileService, UserService


@extend_schema_view(
    post=extend_schema(
        tags=["telegram profiles", "create"],
        operation_id="Create Telegram Profile",
        description="Creates Telegram Profile with supplied parameters.\n"
                    "* Binds telegram profile to user with passed dota_id."
                    "* Creates user if it was not found by dota_id.",
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
        dota_user_id=data["dota_user_id"]
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
        request=GamesAddRequest,
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
def tgprofile_games_synchronise(
        request: Request,
        chat_id: int
) -> HttpResponse:
    TelegramProfileService().synchronise_games(
        chat_id=chat_id
    )
    return HttpResponse("Success", status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        tags=["telegram profiles", "games"],
        operation_id="Retrieve Games",
        description="Retrieve Games filtered by supplied parameters.\n\n"
                    "By default returns all Games sorted by their date.",
        parameters=[
            TopQueryParameter,
            MinDateQueryParameter,
            MaxDateQueryParameter,
            LastDaysQueryParameter,
            HeroQueryParameter,
            WinQueryParameter,
        ],
        responses={
            200: PlayerGameResponse().list(),
            406: APIResponse.invalid_query_parameters(),
        }
    ),

    post=extend_schema(
        tags=["telegram profiles", "games"],
        operation_id="Adds All Games",
        description="Adds games requested count of games to user.\n"
                    "* Wrote player stats from game in db.\n"
                    "* Auto-creates game if it does not exist.\n",
        request=GamesAddRequest,
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
@api_view(["GET", "POST"])
def tgprofile_games(
        request: Request,
        chat_id: int
) -> HttpResponse:
    match request.method:
        case "GET":
            top = parse_query_parameter(request, TopQueryParameter)
            min_date = parse_query_parameter(request, MinDateQueryParameter)
            max_date = parse_query_parameter(request, MaxDateQueryParameter)
            last_days = parse_query_parameter(request, LastDaysQueryParameter)
            hero = parse_query_parameter(request, HeroQueryParameter)
            win = parse_query_parameter(request, WinQueryParameter)

            player_stats = TelegramProfileService().filter_games_stats(
                chat_id=chat_id,
                top=top,
                min_date=min_date,
                max_date=max_date,
                last_days=last_days,
                hero=hero,
                win=win,
            )

            return JsonResponse(
                PlayerGameSerializer(player_stats, many=True).data,
                safe=False
            )

        case "POST":
            data = GamesAddRequest(data=request.data)
            data.is_valid(raise_exception=True)
            data = data.validated_data

            TelegramProfileService().add_games(
                chat_id=chat_id,
                count=data["count"]
            )
            return HttpResponse("Success", status=status.HTTP_201_CREATED)
