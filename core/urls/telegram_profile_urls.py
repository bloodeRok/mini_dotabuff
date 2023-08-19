from django.urls import path

from core.app.handlers.telegram_profile_handlers import tgprofiles

urlpatterns = [
    path(
        "",
        tgprofiles,
        name="tgprofiles"
    ),
]
