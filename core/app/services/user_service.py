from django.db import transaction

from core.app.repositories import UserRepository, GameRepository, \
    TelegramProfileRepository
from core.app.repositories.player_stats_repository import PlayerStatsRepository
from core.app.services.helpers.dotabuff_connection import GameData
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

    def bind_game(
            self,
            game_id: int,
            nickname: str,
            user_name: str
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

        player_stats_repository = PlayerStatsRepository()
        game_repository = GameRepository()
        user = self.repository.find_by_name(name=user_name)
        game_data = GameData(game_id=game_id)
        player_results = game_data.get_player_results(nickname=nickname)
        game_date, game_duration = game_data.get_time_fields()

        with transaction.atomic():
            game = game_repository.get_or_create(
                game_id=game_id,
                game_date=game_date,
                game_duration=game_duration
            )
            player_stats_repository.bind_game(
                game=game,
                user=user,
                player_results=player_results
            )
