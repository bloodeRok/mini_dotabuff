from rest_framework import serializers

from core.constants.field_restrictions import NAME_MAX_LENGTH
from core.models import TelegramProfile


class TelegramProfileCreateRequest(serializers.ModelSerializer):
    chat_id = serializers.IntegerField(
        help_text=TelegramProfile._meta.get_field("chat_id").help_text
    )
    nickname = serializers.CharField(
        help_text="The nickname with which the user plays dota.",
        max_length=NAME_MAX_LENGTH
    )

    class Meta:
        model = TelegramProfile
        fields = [
            "chat_id",
            "nickname"
        ]
