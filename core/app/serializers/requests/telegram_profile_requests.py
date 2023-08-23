from rest_framework import serializers

from core.constants.field_restrictions import NAME_MAX_LENGTH
from core.models import TelegramProfile


class TelegramProfileCreateRequest(serializers.ModelSerializer):
    chat_id = serializers.IntegerField(
        help_text=TelegramProfile._meta.get_field("chat_id").help_text
    )
    dotabuff_user_id = serializers.IntegerField(
        help_text="The ID of the user on dotabuff."
    )

    class Meta:
        model = TelegramProfile
        fields = [
            "chat_id",
            "dotabuff_user_id"
        ]


class GameBindRequest(serializers.Serializer):
    game_id = serializers.IntegerField(
        help_text="ID of the game played."
    )

    class Meta:
        fields = [
            "game_id",
        ]
