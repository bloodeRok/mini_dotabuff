from django.core.validators import MinValueValidator
from django.db import models

from core.constants.field_restrictions import NAME_MAX_LENGTH


class PlayerStats(models.Model):
    nickname = models.CharField(
        help_text="Nickname of the player in this game.",
        max_length=NAME_MAX_LENGTH
    )
    win = models.BooleanField(
        help_text="Is player won the game."
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
        related_name="players_stats"
    )
    player = models.ForeignKey(
        "User",
        on_delete=models.PROTECT,
        related_name="game_stats"
    )

    class Meta:
        unique_together = ("game", "player")

    def __repr__(self):
        return f"<Game(" \
               f"pk={self.pk}, " \
               f"nickname={self.nickname}, " \
               f"win={self.win}, " \
               f"hero={self.hero}, " \
               f"kills={self.kills}, " \
               f"deaths={self.deaths}, " \
               f"assists={self.assists}, " \
               f"networth={self.networth}, " \
               f"last_hits={self.last_hits}, " \
               f"denies={self.denies}, " \
               f"gpm={self.gpm}, " \
               f"xpm={self.xpm}, " \
               f"damage={self.damage} " \
               f")>"

    def __str__(self):
        return self.__repr__()
