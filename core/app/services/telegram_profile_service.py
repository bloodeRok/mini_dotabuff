import time
from typing import Optional

from django.db import transaction

from core.app.api_exceptions import UserGamesNotFound, OldLastGame
from core.app.repositories import (
    UserRepository,
    TelegramProfileRepository,
    GameRepository,
)
from core.app.repositories.player_stats_repository import PlayerStatsRepository
from core.app.services.helpers.dotabuff_connection import GameData, PlayerData, \
    GamesData
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
            user_id=user.dotabuff_id
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
    def __get_all_games_ids(user: User) -> list[int]:
        """
        TODO
        """

        return GamesData.get_last_games_ids(
            dotabuff_user_id=user.dotabuff_id,
        )

    def __get_user_by_chat_id(self, chat_id: int) -> User:
        """
        TODO
        """

        tgprofile = self.repository.find_by_chat_id(chat_id=chat_id)
        return UserRepository().find_by_tgprofile(tgprofile=tgprofile)

    def get_or_create(self, chat_id: int, dotabuff_user_id: int) -> str:
        """
        Creates telegram profile with passed chat ID.
        """

        user_repository = UserRepository()
        dotabuff_nickcname = PlayerData.get_nickname(
            dotabuff_user_id=dotabuff_user_id
        )
        user = user_repository.get_or_create(
            dotabuff_user_id=dotabuff_user_id,
            name=dotabuff_nickcname
        )
        if user.name != dotabuff_nickcname:
            user_repository.update_name(
                user=user,
                new_name=dotabuff_nickcname
            )
        self.repository.bind_user(chat_id=chat_id, user=user)
        return dotabuff_nickcname

    def find_by_chat_id(self, chat_id: int) -> TelegramProfile:
        """
        Finds telegram profile via its chat ID.

        :raises TelegramProfileNotFound: when telegram profile not found.
        """

        return self.repository.find_by_chat_id(chat_id=chat_id)

    def synchronise_games(self, chat_id: int):
        """
        TODO

        :raises UserGamesNotFound: when user has no games.
        :raises OldLastGame: when user last game was more than 50 games ago.
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

        all_games_ids = self.__get_all_games_ids(user=user)

        first_registered_index = get_first_registered_index(
            last_game_id=last_game.adding_games,
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
        TODO
        """

        user = self.__get_user_by_chat_id(chat_id=chat_id)
        all_games_ids = self.__get_all_games_ids(user=user)

        with transaction.atomic():
            for game_id in all_games_ids[:count][::-1]:
                self.__bind_game(
                    game_id=game_id,
                    user=user
                )
                for sec in range(1, 15):
                    time.sleep(1)
                    print(f"I slept for {sec} second(s).")
                print(f"I recorded game (id = {game_id}")



