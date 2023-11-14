from rest_framework import serializers

from backend.models import Game
from .player_stats_serializer import ShortPlayerStatsSerializer


class GameSerializer(serializers.ModelSerializer):
    players = serializers.ListSerializer(
        help_text="The players who played the game"
                  " and registered in the db.",
        child=ShortPlayerStatsSerializer(),
        source="players_stats.all"
    )

    class Meta:
        model = Game
        fields = [
            "game_id",
            "game_date",
            "game_duration",
            "players",
        ]
