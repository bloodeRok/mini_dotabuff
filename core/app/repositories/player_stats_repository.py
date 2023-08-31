from typing import Any

from django.db import IntegrityError

from core.app.api_exceptions.conflict import PlayerGameConflict
from core.models import PlayerStats, Game, User


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
                nickname=player_results["nickname"],
                win=player_results["win"],
                hero=player_results["hero"].name,
                kills=player_results["kills"],
                deaths=player_results["deaths"],
                assists=player_results["assists"],
                networth=player_results["networth"],
                last_hits=player_results["last_hits"],
                denies=player_results["denies"],
                gpm=player_results["gpm"],
                xpm=player_results["xpm"],
                damage=player_results["damage"]
            )
        except IntegrityError:
            raise PlayerGameConflict
