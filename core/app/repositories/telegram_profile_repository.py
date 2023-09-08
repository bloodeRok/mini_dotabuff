import datetime
from typing import Optional

from core.app.api_exceptions.not_found import TelegramProfileNotFound
from core.models import User, TelegramProfile


class TelegramProfileRepository:
    model = TelegramProfile

    def bind_user(self, chat_id: int, user: User) -> None:
        """
        Creates telegram profile with passed chat ID or creates one.
        """

        tg_profile = self.model.objects.filter(chat_id=chat_id).first()
        if not tg_profile:
            self.model.objects.create(chat_id=chat_id, user=user)
            return
        tg_profile.user = user
        tg_profile.save()

    def find_by_chat_id(self, chat_id: int) -> TelegramProfile:
        """
        Finds telegram profile via its chat ID.

        :raises TelegramProfileNotFound: when telegram profile not found.
        """

        tg_profile = self.model.objects.filter(chat_id=chat_id).first()
        if not tg_profile:
            raise TelegramProfileNotFound
        return tg_profile

    def filter_games_stats(
            self,
            user: User,
            top: Optional[int] = None,
            min_date: Optional[str] = None,
            max_date: Optional[str] = None,
            last_days: Optional[int] = None,
            hero: Optional[str] = None,
            win: Optional[bool] = None,
    ):
        """
        TODO docstring + ->
        TODO prefetch_related
        """

        games_stats = user.game_stats.all()

        if min_date:
            min_date = datetime.datetime.fromisoformat(min_date)
            games_stats = games_stats.filter_by(game__game_date__gte=min_date)
        if max_date:
            max_date = \
                datetime.datetime.fromisoformat(max_date)\
                + datetime.timedelta(hours=23, minutes=59)
            games_stats = games_stats.filter_by(game__game_date__lte=max_date)

        if last_days:
            last_days = \
                datetime.date.today() - datetime.timedelta(days=last_days)
            games_stats = games_stats.filter_by(game__game_date__gte=last_days)

        if hero:
            games_stats = games_stats.filter_by(hero=hero)

        if win is not None:
            games_stats = games_stats.filter_by(win=win)

        return games_stats.order_by("-game__game_date")[:top]
