import datetime
from typing import Optional

from core.app.api_exceptions.not_found import UserNotFound
from core.models import User, TelegramProfile, Hero


class UserRepository:
    model = User

    @staticmethod
    def __store(user: User):
        user.save()
        user.refresh_from_db()

    def get_or_create(self, dota_user_id: int, name: str) -> User:
        """
        Creates user with passed chat ID or creates one.
        """

        user = self.model.objects.filter(dota_id=dota_user_id).first()
        if not user:
            user = self.model.objects.create(
                dota_id=dota_user_id,
                name=name
            )

        return user

    def find_by_name(self, name: str) -> User:
        """
        Finds user via its name.

        :raises UserNotFound: when user not found.
        """
        user = self.model.objects.filter(name=name).first()
        if not user:
            raise UserNotFound
        return user

    @staticmethod
    def find_by_tgprofile(tgprofile: TelegramProfile) -> User:
        """
        Finds user via its name.

        :raises UserNotFound: when user not found.
        """
        user = tgprofile.user
        if not user:
            raise UserNotFound
        return user

    def update_name(self, user: User, new_name: str) -> None:
        user.name = new_name
        self.__store(user=user)

    @staticmethod
    def filter_games_stats(
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

        games_stats = user.game_stats.filter(marked=True)

        if min_date:
            min_date = datetime.datetime.fromisoformat(min_date)
            games_stats = games_stats.filter(game__game_date__gte=min_date)
        if max_date:
            max_date = \
                datetime.datetime.fromisoformat(max_date)\
                + datetime.timedelta(hours=23, minutes=59)
            games_stats = games_stats.filter(game__game_date__lte=max_date)

        if last_days:
            last_days = \
                datetime.date.today() - datetime.timedelta(days=last_days)
            games_stats = games_stats.filter(game__game_date__gte=last_days)

        if hero:
            games_stats = games_stats.filter(hero=Hero.objects.get(name=hero))

        if win is not None:
            games_stats = games_stats.filter(win=win)

        return games_stats.order_by("-game__game_date")[:top]
