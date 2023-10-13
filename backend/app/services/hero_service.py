from django.db.models import QuerySet

from backend.app.repositories import HeroRepository
from backend.models import Hero


class HeroService:
    repository = HeroRepository()

    def get_heroes(self) -> QuerySet[Hero]:
        return self.repository.get_heroes()
