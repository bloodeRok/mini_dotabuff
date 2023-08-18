from django.urls import path

from core.app.handlers.game_handlers import games_game

urlpatterns = [
    path(
        "<int:game_id>/",
        games_game,
        name="games_game"
    ),
]
