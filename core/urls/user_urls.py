from django.urls import path

from core.app.handlers.user_handlers import user_games, users_user

urlpatterns = [
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
