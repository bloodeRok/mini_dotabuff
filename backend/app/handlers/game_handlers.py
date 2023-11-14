from django.http import HttpResponse, JsonResponse
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request

from backend.app.handlers.schema_extensions import api_examples
from backend.app.handlers.schema_extensions.api_responses import (
    GameResponse,
)
from backend.app.serializers.responses import GameSerializer
from backend.app.services import GameService


@extend_schema_view(
    get=extend_schema(
        tags=["games", "retrieve games"],
        operation_id="Retrieve Game",
        description="Retrieves requested game.",
        responses={
            200: GameResponse().single(),
            404: GameResponse().not_found(
                examples=[
                    api_examples.GameNotFound
                ]
            )
        }
    )
)
@api_view(["GET"])
def games_game(
        request: Request,
        game_id: int
) -> HttpResponse:
    game = GameService().find_by_game_id(game_id=game_id)
    return JsonResponse(GameSerializer(game).data)
