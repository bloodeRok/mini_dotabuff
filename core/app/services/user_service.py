from django.db import transaction

from core.app.repositories import UserRepository, GameRepository, \
    TelegramProfileRepository
from core.app.repositories.player_stats_repository import PlayerStatsRepository
from core.app.services.helpers.open_dota_connection import GameData
from core.models import User, TelegramProfile


class UserService:
    repository = UserRepository()

    def find_by_chat_id(self, chat_id: int) -> User:
        """
        Finds user via its telegram profile.

        :raises UserNotFound: when user not found.
        """

        tgprofile = TelegramProfileRepository().find_by_chat_id(
            chat_id=chat_id
        )

        return self.repository.find_by_tgprofile(tgprofile=tgprofile)
