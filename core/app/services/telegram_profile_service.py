from typing import Optional

from django.db import transaction

from core.app.api_exceptions import UserGamesNotFound, OldLastGame
from core.app.repositories import (
    UserRepository,
    TelegramProfileRepository,
    GameRepository,
)
from core.app.repositories import PlayerStatsRepository
from core.app.services.helpers.open_dota_connection import (
    GameData,
    PlayerData,
    GamesData,
)
from core.models import TelegramProfile, User


class TelegramProfileService:
    repository = TelegramProfileRepository()

    @staticmethod
    def __bind_game(
            game_id: int,
            user: User
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

        game_data = GameData(game_id=game_id)
        player_results = game_data.get_player_results(
            nickname=user.name,
            dota_id=user.dota_id
        )

        if player_results is None:
            return

        game_date, game_duration = game_data.get_time_fields()

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

    @staticmethod
    def __get_games_ids(user: User, count: Optional[int] = 50) -> list[int]:
        """
        Returns the requested number of IDs of last games.

        :raises NotAcceptable: when user_id is invalid
        """

        return GamesData.get_last_games_ids(
            dota_id=user.dota_id,
            count=count
        )

    def __get_user_by_chat_id(self, chat_id: int) -> User:
        """
        Returns user by requested chat ID.

        :raises TelegramProfileNotFound: when telegram profile not found.
        :raises UserNotFound: when user not found.
        """

        tgprofile = self.repository.find_by_chat_id(chat_id=chat_id)
        return UserRepository().find_by_tgprofile(tgprofile=tgprofile)

    def get_or_create(self, chat_id: int, dota_user_id: int) -> str:
        """
        Creates telegram profile with passed chat ID.
        """

        user_repository = UserRepository()
        dota_nickcname = PlayerData.get_nickname(
            dota_user_id=dota_user_id
        )
        user = user_repository.get_or_create(
            dota_user_id=dota_user_id,
            name=dota_nickcname
        )
        if user.name != dota_nickcname:
            user_repository.update_name(
                user=user,
                new_name=dota_nickcname
            )
        self.repository.bind_user(chat_id=chat_id, user=user)
        return dota_nickcname

    def find_by_chat_id(self, chat_id: int) -> TelegramProfile:
        """
        Finds telegram profile via its chat ID.

        :raises TelegramProfileNotFound: when telegram profile not found.
        """

        return self.repository.find_by_chat_id(chat_id=chat_id)

    def synchronise_games(self, chat_id: int):
        """
        Synchronises user's games.

        :raises UserGamesNotFound: when user has no games.
        :raises OldLastGame: when user last game was more than 50 games ago.
        :raises TelegramProfileNotFound: when telegram profile not found.
        :raises UserNotFound: when user not found.
        :raises NotAcceptable: when game_id is invalid
        :raises PlayerNotFoundException: when nickname
            was not found in game.
        :raises PlayerGameConflict: when player
            already registered in this game.
        """

        def get_first_registered_index(
                last_game_id: int,
                games_ids: list[int]
        ) -> Optional[int]:
            for index, game_id in enumerate(games_ids):
                if last_game_id == game_id:
                    return index
            return None

        user = self.__get_user_by_chat_id(chat_id=chat_id)

        last_game = user.games.last()
        if last_game is None:
            raise UserGamesNotFound

        all_games_ids = self.__get_games_ids(user=user)

        first_registered_index = get_first_registered_index(
            last_game_id=last_game.game_id,
            games_ids=all_games_ids
        )

        if first_registered_index is None:
            raise OldLastGame

        with transaction.atomic():
            for game_id in all_games_ids[:first_registered_index][::-1]:
                self.__bind_game(
                    game_id=game_id,
                    user=user
                )

    def add_games(self, chat_id: int, count: int) -> None:
        """
        Adds requested count of games to a user found via chat ID.

        :raises TelegramProfileNotFound: when telegram profile not found.
        :raises UserNotFound: when user not found.
        :raises NotAcceptable: when data is invalid
            or Open Dota API is unavailable.
        :raises UserNotFound: when user not found.
        :raises PlayerNotFoundException: when nickname
            was not found in game.
        :raises PlayerGameConflict: when player
            already registered in this game.
        """

        user = self.__get_user_by_chat_id(chat_id=chat_id)
        all_games_ids = self.__get_games_ids(
            user=user,
            count=count
        )

        with transaction.atomic():
            for game_id in all_games_ids[:count][::-1]:
                self.__bind_game(
                    game_id=game_id,
                    user=user
                )

    def filter_games_stats(
            self,
            chat_id: int,
            top: Optional[int] = None,
            min_date: Optional[str] = None,
            max_date: Optional[str] = None,
            last_days: Optional[int] = None,
            hero: Optional[str] = None,
            win: Optional[bool] = None,
    ):
        """
        TODO docstring + ->
        """

        user = self.__get_user_by_chat_id(chat_id=chat_id)
        player_stats = UserRepository().filter_games_stats(
            user=user,
            top=top,
            min_date=min_date,
            max_date=max_date,
            last_days=last_days,
            hero=hero,
            win=win,
        )

        return player_stats
