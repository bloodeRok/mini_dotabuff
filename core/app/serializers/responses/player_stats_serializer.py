from rest_framework import serializers

from core.models import PlayerStats


class ShortPlayerStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayerStats
        fields = [
            "nickname",
            "hero",
        ]


class FullPlayerStatsSerializer(ShortPlayerStatsSerializer):
    class Meta:
        model = PlayerStats
        fields = ShortPlayerStatsSerializer.Meta.fields + [
            "win",
            "kills",
            "deaths",
            "assists",
            "networth",
            "last_hits",
            "denies",
            "gpm",
            "xpm",
            "damage",
        ]
