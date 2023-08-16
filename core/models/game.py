from django.db import models


class Game(models.Model):
    game_id = models.IntegerField(
        help_text="ID of the game.",
        unique=True
    )

    def __repr__(self):
        return f"<Game(" \
               f"pk={self.pk}, " \
               f"game_id={self.game_id} " \
               f")>"

    def __str__(self):
        return self.__repr__()