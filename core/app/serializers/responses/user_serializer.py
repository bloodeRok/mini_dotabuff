from typing import Optional

from django.db.models import Count, Avg
from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    matches_recorded = serializers.IntegerField(
        help_text="Number of recorded matches.",
        source="games.count"
    )
    win_rate = serializers.SerializerMethodField(
        help_text="User's win rate."
    )
    favorite_hero = serializers.SerializerMethodField(
        help_text="User's favorite hero."
    )
    avg_gpm = serializers.SerializerMethodField(
        help_text="User's average gold per minute."
    )
    avg_xpm = serializers.SerializerMethodField(
        help_text="User's average experience per minute."
    )
    avg_kda = serializers.SerializerMethodField(
        help_text="User's average kills/deaths/assists."
    )

    @staticmethod
    def get_win_rate(user: User) -> Optional[str]:
        all_stats = user.game_stats.all()
        wr = all_stats.filter(win=True).count() / all_stats.count()
        return str(round(wr, 3) * 100) + " %" if wr else None

    @staticmethod
    def get_favorite_hero(user: User) -> Optional[str]:
        return user.game_stats. \
            values("hero").annotate(total=Count('id')). \
            order_by("-total").first()["hero"]

    @staticmethod
    def get_avg_gpm(user: User) -> Optional[int]:
        return int(user.game_stats.aggregate(avg=Avg("gpm"))["avg"])

    @staticmethod
    def get_avg_xpm(user: User) -> Optional[int]:
        return int(user.game_stats.aggregate(avg=Avg("xpm"))["avg"])

    @staticmethod
    def get_avg_kda(user: User) -> Optional[int]:
        kills = user.game_stats.aggregate(sum=Avg("kills"))["sum"]
        deaths = user.game_stats.aggregate(sum=Avg("deaths"))["sum"]
        assists = user.game_stats.aggregate(sum=Avg("assists"))["sum"]
        return round((kills + assists) / deaths, 1)

    class Meta:
        model = User
        fields = [
            "name",
            "matches_recorded",
            "win_rate",
            "favorite_hero",
            "avg_gpm",
            "avg_xpm",
            "avg_kda",
        ]
