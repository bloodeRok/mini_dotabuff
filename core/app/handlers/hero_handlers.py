from django.http import HttpResponse, JsonResponse
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request

from core.app.handlers.schema_extensions.api_responses import HeroResponse
from core.app.serializers.responses import HeroSerializer
from core.app.services import HeroService


@extend_schema_view(
    get=extend_schema(
        tags=["heroes"],
        operation_id="Retrieve Heroes",
        description="Retrieves all heroes from db.",
        responses={
            200: HeroResponse().list()
        }
    )
)
@api_view(["GET"])
def heroes(
        request: Request
) -> HttpResponse:
    all_heroes = HeroService().get_heroes()

    return JsonResponse(HeroSerializer(all_heroes, many=True).data, safe=False)
