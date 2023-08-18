from rest_framework import serializers

from core.constants.field_restrictions import NAME_MAX_LENGTH
from core.models import User


class UserCreateRequest(serializers.ModelSerializer):
    name = serializers.CharField(
        help_text=User._meta.get_field("name").help_text
    )

    class Meta:
        model = User
        fields = [
            "name"
        ]


class GameBindRequest(serializers.ModelSerializer):
    game_id = serializers.IntegerField(
        help_text="ID of the game played."
    )
    dota_nickname = serializers.CharField(
        help_text="Nickname of the player he played the game with.",
        max_length=NAME_MAX_LENGTH
    )

    class Meta:
        model = User
        fields = [
            "game_id",
            "dota_nickname"
        ]
