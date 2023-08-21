from django.db import IntegrityError

from core.app.api_exceptions import UserConflict
from core.app.api_exceptions.not_found import UserNotFound
from core.models import User, Game, TelegramProfile


class UserRepository:
    model = User

    def get_or_create(self, name: str) -> User:
        """
        Creates user with passed chat ID or creates one.
        """

        user = self.model.objects.filter(name=name).first()
        if not user:
            user = self.model.objects.create(name=name)
        return user

    def find_by_name(self, name: str) -> User:
        """
        Finds user via its name.

        :raises UserNotFound: when user not found.
        """
        user = self.model.objects.filter(name=name).first()
        if not user:
            raise UserNotFound
        return user

    @staticmethod
    def find_by_tgprofile(tgprofile: TelegramProfile) -> User:
        """
        Finds user via its name.

        :raises UserNotFound: when user not found.
        """
        user = tgprofile.user
        if not user:
            raise UserNotFound
        return user
