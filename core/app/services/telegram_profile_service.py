from django.db import transaction

from core.app.repositories import UserRepository, TelegramProfileRepository, \
    GameRepository
from core.app.repositories.player_stats_repository import PlayerStatsRepository
from core.app.services.helpers.dotabuff_connection import GameData
from core.models import TelegramProfile


class TelegramProfileService:
    repository = TelegramProfileRepository()

    def get_or_create(self, chat_id: int, nickname: str) -> None:
        """
        Creates telegram profile with passed chat ID.
        """

        user = UserRepository().get_or_create(name=nickname)
        self.repository.bind_user(chat_id=chat_id, user=user)

    def find_by_chat_id(self, chat_id: int) -> TelegramProfile:
        """
        Finds telegram profile via its chat ID.

        :raises TelegramProfileNotFound: when telegram profile not found.
        """

        return self.repository.find_by_chat_id(chat_id=chat_id)

    def bind_game(
            self,
            game_id: int,
            chat_id: int
    ) -> None:
        """
        Binds the game to the passed user.
        Adds users results of this game to the db.

        :raises UserNotFound: when user not found.
        :raises NotAcceptable: when game_id is invalid
        :raises PlayerNotFoundException: when nickname
                 was not found in game.
        :raises PlayerGameConflict: when player
                 already registered in this game.

        """

        tgprofile = self.repository.find_by_chat_id(chat_id=chat_id)
        user = UserRepository().find_by_tgprofile(tgprofile=tgprofile)
        game_data = GameData(game_id=game_id)
        player_results = game_data.get_player_results(
            nickname=user.name
        )
        game_date, game_duration = game_data.get_time_fields()

        with transaction.atomic():
            game = GameRepository().get_or_create(
                game_id=game_id,
                game_date=game_date,
                game_duration=game_duration
            )
            PlayerStatsRepository().bind_game(
                game=game,
                user=user,
                player_results=player_results
            )
