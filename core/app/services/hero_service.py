from django.db.models import QuerySet

from core.app.repositories import HeroRepository
from core.models import Hero


class HeroService:
    repository = HeroRepository()

    def get_heroes(self) -> QuerySet[Hero]:
        return self.repository.get_heroes()
