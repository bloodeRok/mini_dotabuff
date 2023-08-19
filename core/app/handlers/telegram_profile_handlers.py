from django.http import HttpResponse
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request

from core.app.handlers.schema_extensions.api_responses import (
    TelegramProfileResponse,
)
from core.app.serializers.requests import TelegramProfileCreateRequest
from core.app.services import TelegramProfileService


@extend_schema_view(
    post=extend_schema(
        tags=["telegram profiles", "create"],
        operation_id="Create Telegram Profile",
        description="Creates Telegram Profile with supplied parameters.\n"
                    "* Creates user if it was not found by nickname.",
        request=TelegramProfileCreateRequest,
        responses={
            201: TelegramProfileResponse().created()
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

    TelegramProfileService().get_or_create(
        chat_id=data["chat_id"],
        nickname=data["nickname"]
    )
    return HttpResponse("Success", status=status.HTTP_201_CREATED)
