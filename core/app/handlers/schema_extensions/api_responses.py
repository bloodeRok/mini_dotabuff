from typing import List, Type

from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from rest_framework.serializers import ModelSerializer

from core.app.handlers.schema_extensions import api_examples
from core.app.serializers.responses import (
    APIErrorSerializer,
    GameSerializer,
    UserSerializer, TelegramProfileSerializer,
)


class APIResponse:
    serializer: Type[ModelSerializer]
    entity_name: str
    title_entity_name: str
    plural_entity_name: str

    def single(self) -> OpenApiResponse:
        return OpenApiResponse(
            response=self.serializer,
            description=f"Requested {self.entity_name} data."
        )

    def created(self) -> OpenApiResponse:
        return OpenApiResponse(
            response=str,
            description=f"{self.title_entity_name} successfully created.",
            examples=[api_examples.Success]
        )

    def updated(self) -> OpenApiResponse:
        return OpenApiResponse(
            response=None,
            description=f"{self.title_entity_name} successfully updated."
        )

    def not_found(
            self,
            examples: List[OpenApiExample] = None
    ) -> OpenApiResponse:
        return OpenApiResponse(
            response=APIErrorSerializer,
            description=f"{self.title_entity_name} could not be found"
                        " via supplied parameters.",
            examples=examples
        )

    def conflict(
            self,
            examples: List[OpenApiExample] = None
    ) -> OpenApiResponse:
        return OpenApiResponse(
            response=APIErrorSerializer,
            description=f"{self.title_entity_name} with supplied"
                        " identification parameters already exists.",
            examples=examples
        )

    @staticmethod
    def invalid_parameters(
            examples: List[OpenApiExample] = None
    ) -> OpenApiResponse:
        return OpenApiResponse(
            response=APIErrorSerializer,
            description="Request parameters are invalid.",
            examples=examples
        )


class UserResponse(APIResponse):
    serializer = UserSerializer
    entity_name = "user"
    title_entity_name = "User"
    plural_entity_name = "users"


class GameResponse(APIResponse):
    serializer = GameSerializer
    entity_name = "game"
    title_entity_name = "Game"
    plural_entity_name = "games"


class TelegramProfileResponse(APIResponse):
    serializer = TelegramProfileSerializer
    entity_name = "telegram profile"
    title_entity_name = "Telegram profile"
    plural_entity_name = "telegram profiles"
