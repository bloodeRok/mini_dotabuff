from django.urls import path

from core.app.handlers.user_handlers import users, user_games, users_user

urlpatterns = [
    path(
        "",
        users,
        name="users",
    ),
    path(
        "<str:name>/",
        users_user,
        name="users_user"
    ),
    path(
        "<str:name>/games/",
        user_games,
        name="user_games"
    )
]
