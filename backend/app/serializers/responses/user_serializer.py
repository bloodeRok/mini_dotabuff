from typing import Optional

from django.db.models import Count, Avg
from rest_framework import serializers

from backend.models import User, Hero


class UserSerializer(serializers.ModelSerializer):
    matches_recorded = serializers.SerializerMethodField(
        help_text="Number of recorded matches."
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
        help_text="User's average kills/deaths/assists stats."
    )

    @staticmethod
    def get_matches_recorded(user: User):
        return user.game_stats.filter(marked=True).count()

    @staticmethod
    def get_win_rate(user: User) -> Optional[str]:
        all_stats = user.game_stats.filter(marked=True)
        try:
            wr = all_stats.filter(win=True).count() / all_stats.count()
            return str(round(wr * 100, 1)) + " %"
        except ZeroDivisionError:
            return None

    @staticmethod
    def get_favorite_hero(user: User) -> Optional[str]:
        if user.game_stats.filter(marked=True).count() > 0:
            hero_id = user.game_stats.filter(marked=True). \
                values("hero").annotate(total=Count('id')). \
                order_by("-total").first()["hero"]
            return Hero.objects.get(id=hero_id).name
        return None

    @staticmethod
    def get_avg_gpm(user: User) -> Optional[int]:
        if user.game_stats.filter(marked=True).count() > 0:
            return int(user.game_stats.aggregate(avg=Avg("gpm"))["avg"])
        return None

    @staticmethod
    def get_avg_xpm(user: User) -> Optional[int]:
        if user.game_stats.filter(marked=True).count() > 0:
            return int(user.game_stats.aggregate(avg=Avg("xpm"))["avg"])
        return None

    @staticmethod
    def get_avg_kda(user: User) -> Optional[int]:
        kills = user.game_stats.filter(marked=True). \
            aggregate(sum=Avg("kills"))["sum"]
        deaths = user.game_stats.filter(marked=True). \
            aggregate(sum=Avg("deaths"))["sum"]
        assists = user.game_stats.filter(marked=True). \
            aggregate(sum=Avg("assists"))["sum"]
        result = []
        if kills:
            result.append(kills)
        if assists:
            result.append(assists)
        if deaths:
            return round(sum(result) / deaths, 1)
        if len(result) == 0:
            return None
        return sum(result)

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
