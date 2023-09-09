import datetime
from typing import Optional

from core.app.api_exceptions.not_found import TelegramProfileNotFound
from core.models import User, TelegramProfile


class TelegramProfileRepository:
    model = TelegramProfile

    def bind_user(self, chat_id: int, user: User) -> None:
        """
        Creates telegram profile with passed chat ID or creates one.
        """

        tg_profile = self.model.objects.filter(chat_id=chat_id).first()
        if not tg_profile:
            self.model.objects.create(chat_id=chat_id, user=user)
            return
        tg_profile.user = user
        tg_profile.save()

    def find_by_chat_id(self, chat_id: int) -> TelegramProfile:
        """
        Finds telegram profile via its chat ID.

        :raises TelegramProfileNotFound: when telegram profile not found.
        """

        tg_profile = self.model.objects.filter(chat_id=chat_id).first()
        if not tg_profile:
            raise TelegramProfileNotFound
        return tg_profile
