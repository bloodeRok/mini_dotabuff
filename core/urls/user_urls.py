from django.urls import path

from core.app.handlers.user_handlers import user_games

urlpatterns = [
    path(
        "<str:name>/games/",
        user_games,
        name="user_games"
    )
]
