from django.db.models import QuerySet

from backend.models import Hero


class HeroRepository:
    model = Hero

    def get_heroes(self) -> QuerySet[Hero]:
        return self.model.objects.all().order_by("name")
