from django.db import models

from core.constants.field_restrictions import NAME_MAX_LENGTH


class Hero(models.Model):
    name = models.CharField(
        help_text="Name of the user.",
        max_length=NAME_MAX_LENGTH,
        unique=True
    )
    hero_id = models.IntegerField(
        help_text="ID of the hero on Open Dota.",
        unique=True
    )

    def __repr__(self):
        return f"<User(" \
               f"pk={self.pk}, " \
               f"name={self.name}, " \
               f"hero_id={self.hero_id} " \
               f")>"

    def __str__(self):
        return self.__repr__()
