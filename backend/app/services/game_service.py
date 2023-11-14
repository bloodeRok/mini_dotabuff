from backend.app.repositories import GameRepository
from backend.models import Game


class GameService:
    repository = GameRepository()

    def find_by_game_id(self, game_id: int) -> Game:
        """
        Finds game via its game_id.

        :raises GameNotFound: when game not found.
        """

        return self.repository.find_by_game_id(game_id=game_id)
