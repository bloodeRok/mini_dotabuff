from rest_framework import serializers

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
