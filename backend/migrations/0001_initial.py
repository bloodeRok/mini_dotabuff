# Generated by Django 4.2.3 on 2023-09-11 11:53

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion

from backend.constants.defaults import ADD_HEROES_MIGRATION_SQL


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Game",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "game_id",
                    models.BigIntegerField(help_text="ID of the game.", unique=True),
                ),
                (
                    "game_date",
                    models.DateTimeField(help_text="Date of the game played."),
                ),
                ("game_duration", models.TimeField(help_text="Game duration.")),
            ],
        ),
        migrations.CreateModel(
            name="Hero",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the hero.", max_length=63, unique=True
                    ),
                ),
                (
                    "hero_id",
                    models.IntegerField(
                        db_index=True,
                        help_text="ID of the hero on Open Dota.",
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.RunSQL(
            sql=ADD_HEROES_MIGRATION_SQL,
            reverse_sql="",
        ),
        migrations.CreateModel(
            name="PlayerStats",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("win", models.BooleanField(help_text="Is player won the game.")),
                (
                    "kills",
                    models.IntegerField(
                        help_text="The number of kills made by the player.",
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "deaths",
                    models.IntegerField(
                        help_text="The number of deaths by player.",
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "assists",
                    models.IntegerField(
                        help_text="The number of assists by playere.",
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "networth",
                    models.IntegerField(
                        help_text="The amount of gold earned by the player.",
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "last_hits",
                    models.IntegerField(
                        help_text="The number of last hits creeps by the player.",
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "denies",
                    models.IntegerField(
                        help_text="The number of denied creeps by the player.",
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "gpm",
                    models.IntegerField(
                        help_text="The amount of gold per minute earned by the player.",
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "xpm",
                    models.IntegerField(
                        help_text="The amount of experience per minute earned by the player.",
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "damage",
                    models.IntegerField(
                        help_text="The amount of damage dealt by the player.",
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "marked",
                    models.BooleanField(default=True, help_text="Games to show"),
                ),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="players_stats",
                        to="backend.game",
                    ),
                ),
                (
                    "hero",
                    models.ForeignKey(
                        help_text="The hero the player played on.",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="backend.hero",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the user.", max_length=63, unique=True
                    ),
                ),
                (
                    "dota_id",
                    models.IntegerField(
                        help_text="ID of the user in DOTA 2.", unique=True
                    ),
                ),
                (
                    "games",
                    models.ManyToManyField(through="backend.PlayerStats", to="backend.game"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TelegramProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "chat_id",
                    models.IntegerField(help_text="Chat ID of the user.", unique=True),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="chat_ids",
                        to="backend.user",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="playerstats",
            name="player",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="game_stats",
                to="backend.user",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="playerstats",
            unique_together={("game", "player")},
        ),
    ]
