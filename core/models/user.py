from django.db import models

from core.constants.field_restrictions import NAME_MAX_LENGTH


class User(models.Model):
    name = models.CharField(
        help_text="Name of the user.",
        max_length=NAME_MAX_LENGTH
    )

    #  Relationships.
    games = models.ManyToManyField(
        "Game",
        through="UsersGames"
    )

    def __repr__(self):
        return f"<Game(" \
               f"pk={self.pk}, " \
               f"name={self.name} " \
               f")>"

    def __str__(self):
        return self.__repr__()