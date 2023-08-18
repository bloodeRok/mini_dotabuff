from django.db import models


class Game(models.Model):
    game_id = models.BigIntegerField(
        help_text="ID of the game.",
        unique=True
    )
    game_date = models.DateTimeField(
        help_text="Date of the game played."
    )
    game_duration = models.TimeField(
        help_text="Game duration."
    )

    def __repr__(self):
        return f"<Game(" \
               f"pk={self.pk}, " \
               f"game_id={self.game_id}, " \
               f"game_date={self.game_date}, " \
               f"game_duration={self.game_duration}" \
               f")>"

    def __str__(self):
        return self.__repr__()