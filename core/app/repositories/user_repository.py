from django.db import IntegrityError

from core.app.api_exceptions import UserConflict
from core.app.api_exceptions.not_found import UserNotFound
from core.models import User, Game


class UserRepository:
    model = User

    def create(self, name: str) -> User:
        """
        Creates user with passed name.

        :raises UserConflict: when user already exists.
        """

        try:
            return self.model.objects.create(name=name)
        except IntegrityError:
            raise UserConflict

    def find_by_name(self, name: str) -> User:
        """
        Finds user via its name.

        :raises UserNotFound: when user not found.
        """
        user = self.model.objects.filter(name=name).first()
        if not user:
            raise UserNotFound
        return user
