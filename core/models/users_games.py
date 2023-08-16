from django.core.validators import MinValueValidator
from django.db import models

from core.constants.field_restrictions import NAME_MAX_LENGTH


class UsersGames(models.Model):
    nickname = models.CharField(
        help_text="Nickname of the player in this game.",
        max_length=NAME_MAX_LENGTH
    )
    hero = models.CharField(
        help_text="The hero the player played on.",
        max_length=NAME_MAX_LENGTH
    )
    kills = models.IntegerField(
        help_text="The number of kills made by the player.",
        validators=[
            MinValueValidator(0)
        ]
    )
    deaths = models.IntegerField(
        help_text="The number of deaths by player.",
        validators=[
            MinValueValidator(0)
        ]
    )
    assists = models.IntegerField(
        help_text="The number of assists by playere.",
        validators=[
            MinValueValidator(0)
        ]
    )
    networth = models.IntegerField(
        help_text="The amount of gold earned by the player.",
        validators=[
            MinValueValidator(0)
        ]
    )
    last_hits = models.IntegerField(
        help_text="The number of last hits creeps by the player.",
        validators=[
            MinValueValidator(0)
        ]
    )
    denies = models.IntegerField(
        help_text="The number of denied creeps by the player.",
        validators=[
            MinValueValidator(0)
        ]
    )
    gpm = models.IntegerField(
        help_text="The amount of gold per minute earned by the player.",
        validators=[
            MinValueValidator(0)
        ]
    )
    xpm = models.IntegerField(
        help_text="The amount of experience per minute earned by the player.",
        validators=[
            MinValueValidator(0)
        ]
    )
    damage = models.IntegerField(
        help_text="The amount of damage dealt by the player.",
        validators=[
            MinValueValidator(0)
        ]
    )

    # Relationships.
    game = models.ForeignKey(
        "Game",
        on_delete=models.PROTECT,
        related_name="games"
    )
    player = models.ForeignKey(
        "User",
        on_delete=models.PROTECT,
        related_name="players"
    )
