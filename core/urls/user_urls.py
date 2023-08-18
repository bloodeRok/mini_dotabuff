from django.urls import path

from core.app.handlers.user_handlers import users, user_games

urlpatterns = [
    path(
        "",
        users,
        name="users",
    ),
    path(
        "<str:name>/games/",
        user_games,
        name="user_games"
    )
]