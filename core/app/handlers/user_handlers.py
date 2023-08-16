from django.http import HttpResponse
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request

from core.app.serializers.requests import UserCreateRequest
from core.app.services import UserService


@extend_schema_view(
    post=extend_schema(
        tags=["users", "create"],
        operation_id="Create User",
        description="Creates User with supplied parameters.",
        request=UserCreateRequest,
        # responses={
        #     201: UserResponse().created(),
        #     404: UserResponse().related_not_found(
        #         examples=[
        #             api_examples.BlockchainNotFound
        #         ]
        #     ),
        #     406: APIResponse.invalid_parameters(
        #         examples=[
        #             api_examples.InvalidMetadata,
        #             api_examples.InvalidAddress
        #         ]
        #     ),
        #     409: NFTResponse().conflict(
        #         examples=[api_examples.TokenExists]
        #     ),
        # }
    )
)
@api_view(["POST"])
def users(
        request: Request
) -> HttpResponse:
    data = UserCreateRequest(data=request.data)
    data.is_valid(raise_exception=True)
    data = data.validated_data

    UserService().create(
        name=data["name"]
    )
    return HttpResponse("Success", status=status.HTTP_201_CREATED)
