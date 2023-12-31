from rest_framework import serializers

from backend.models import Hero


class HeroSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hero
        fields = [
            "name"
        ]
