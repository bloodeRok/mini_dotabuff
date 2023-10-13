from rest_framework import serializers

from backend.models import PlayerStats, Hero


class ShortPlayerStatsSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(
        help_text="Nickname of the player.",
        source="user.name"
    )

    class Meta:
        model = PlayerStats
        fields = [
            "nickname",  # TODO
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


class PlayerGameSerializer(serializers.ModelSerializer):
    hero = serializers.CharField(
        help_text=Hero._meta.get_field("name").help_text,
        source="hero.name"
    )
    game_date = serializers.DateTimeField(
        help_text="Date and time when the game was played.",
        source="game.game_date"
    )
    game_duration = serializers.DateTimeField(
        help_text="Duration of the game.",
        source="game.game_duration"
    )
    KDA = serializers.SerializerMethodField(
        help_text="Player's KDA (kills/deaths/assists)."
    )

    @staticmethod
    def get_KDA(player_stats: PlayerStats) -> str:
        kills = player_stats.kills
        deaths = player_stats.deaths
        assists = player_stats.assists
        return f"{kills}/{deaths}/{assists}"

    class Meta:
        model = PlayerStats
        fields = [
            "hero",
            "win",
            "game_date",
            "game_duration",
            "KDA"
        ]
