from django.urls import path

from core.app.handlers.telegram_profile_handlers import (
    tgprofiles,
    tgprofiles_users_user,
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
]
