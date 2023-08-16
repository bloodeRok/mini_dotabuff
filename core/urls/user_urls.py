from django.urls import path

from core.app.handlers.user_handlers import users

urlpatterns = [
    path(
        "",
        users,
        name="users",
    )
]