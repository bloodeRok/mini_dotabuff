from django.urls import path

from backend.app.handlers.hero_handlers import heroes

urlpatterns = [
    path(
        "",
        heroes,
        name="heroes"
    ),
]
