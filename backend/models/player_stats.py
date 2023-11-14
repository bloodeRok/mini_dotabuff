from django.core.validators import MinValueValidator
from django.db import models

from backend.constants.field_restrictions import NAME_MAX_LENGTH


class PlayerStats(models.Model):
    win = models.BooleanField(
        help_text="Is player won the game."
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
    marked = models.BooleanField(
        help_text="Games to show",
        default=True
    )

    # Relationships.
    hero = models.ForeignKey(
        to="Hero",
        help_text="The hero the player played on.",
        on_delete=models.PROTECT
    )
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
               f"nickname={self.player.name}, " \
               f"win={self.win}, " \
               f"hero={self.hero.name}, " \
               f"kills={self.kills}, " \
               f"deaths={self.deaths}, " \
               f"assists={self.assists}, " \
               f"networth={self.networth}, " \
               f"last_hits={self.last_hits}, " \
               f"denies={self.denies}, " \
               f"gpm={self.gpm}, " \
               f"xpm={self.xpm}, " \
               f"damage={self.damage}, " \
               f"marked={self.marked} " \
               f")>"

    def __str__(self):
        return self.__repr__()
