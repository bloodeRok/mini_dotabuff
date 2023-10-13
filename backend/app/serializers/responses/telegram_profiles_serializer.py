from rest_framework import serializers

from backend.models import TelegramProfile


class TelegramProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(
        help_text="The nickname to which this chat is linked.",
        source="user"
    )

    class Meta:
        model = TelegramProfile
        fields = [
            "chat_id",
            "user",
        ]
