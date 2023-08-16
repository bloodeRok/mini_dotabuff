from django.db import IntegrityError

from core.app.api_exceptions import UserConflict
from core.models import User


class UserRepository:
    model = User

    def create(self, name: str) -> User:
        try:
            return self.model.objects.create(name=name)
        except IntegrityError:
            raise UserConflict
