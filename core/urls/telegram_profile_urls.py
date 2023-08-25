from django.urls import path

from core.app.handlers.telegram_profile_handlers import (
    tgprofiles,
    tgprofile_games,
    tgprofiles_users_user,
    tgprofile_games_synchronise
)

urlpatterns = [
    path(
        "<int:chat_id>/user/",
        tgprofiles_users_user,
        name="tgprofiles_user"
    ),
    path(
        "",
        tgprofiles,
        name="tgprofiles"
    ),
    path(
        "<int:chat_id>/games/synchronise/",
        tgprofile_games_synchronise,
        name="tgprofile_games_synchronise"
    ),
    path(
        "<int:chat_id>/games/",
        tgprofile_games,
        name="tgprofile_games"
    )
]
