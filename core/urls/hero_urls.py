from django.urls import path

from core.app.handlers.hero_handlers import heroes

urlpatterns = [
    path(
        "",
        heroes,
        name="heroes"
    ),
]
