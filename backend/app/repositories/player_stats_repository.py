from typing import Any

from django.db import IntegrityError

from bot.core.constants.bot_constants import ADMIN_ACCOUNT
from backend.app.api_exceptions.conflict import PlayerGameConflict
from backend.models import PlayerStats, Game, User


class PlayerStatsRepository:
    model = PlayerStats

    def bind_game(
            self,
            game: Game,
            user: User,
            player_results: dict[str, Any]
    ) -> None:
        """
        Binds the game to the user.
        Adds the results to the intermediate table.

        :raises PlayerGameConflict: when player
                already registered in this game.
        """

        try:
            self.model.objects.create(
                game=game,
                player=user,
                win=player_results["win"],
                hero=player_results["hero"],
                kills=player_results["kills"],
                deaths=player_results["deaths"],
                assists=player_results["assists"],
                networth=player_results["networth"],
                last_hits=player_results["last_hits"],
                denies=player_results["denies"],
                gpm=player_results["gpm"],
                xpm=player_results["xpm"],
                damage=player_results["damage"],
                marked=False if user.dota_id == ADMIN_ACCOUNT else True
            )
        except IntegrityError:
            raise PlayerGameConflict
