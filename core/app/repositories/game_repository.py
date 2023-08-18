from core.models import User, Game
from datetime import datetime, time


class GameRepository:
    model = Game

    def get_or_create(
            self,
            game_id: int,
            game_date: datetime,
            game_duration
    ) -> Game:
        """
        Retrieves game via its game_id
        or creates one with passed game_date and game_duration.
        """

        game = self.model.objects.filter(game_id=game_id).first()
        if game:
            return game
        return self.model.objects.create(
            game_id=game_id,
            game_date=game_date,
            game_duration=game_duration
        )
