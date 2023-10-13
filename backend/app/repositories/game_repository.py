import datetime

from backend.app.api_exceptions import GameNotFound
from backend.models import Game


class GameRepository:
    model = Game

    def get_or_create(
            self,
            game_id: int,
            game_date: datetime.datetime,
            game_duration: datetime.time
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

    def find_by_game_id(self, game_id: int) -> Game:
        """
        Finds game via its game_id.

        :raises GameNotFound: when game not found.
        """

        game = self.model.objects.filter(game_id=game_id).first()
        if not game:
            raise GameNotFound
        return game
