from django.db import models

from backend.constants.field_restrictions import NAME_MAX_LENGTH


class User(models.Model):
    name = models.CharField(
        help_text="Name of the user.",
        max_length=NAME_MAX_LENGTH,
        unique=True
    )
    dota_id = models.IntegerField(
        help_text="ID of the user in DOTA 2.",
        unique=True
    )

    #  Relationships.
    games = models.ManyToManyField(
        "Game",
        through="PlayerStats"
    )

    def __repr__(self):
        return f"<User(" \
               f"pk={self.pk}, " \
               f"dota_id={self.dota_id}, " \
               f"name={self.name} " \
               f")>"

    def __str__(self):
        return self.__repr__()
