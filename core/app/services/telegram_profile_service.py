from core.app.repositories import UserRepository, TelegramProfileRepository
from core.models import TelegramProfile


class TelegramProfileService:
    repository = TelegramProfileRepository()

    def get_or_create(self, chat_id: int, nickname: str) -> None:
        """
        Creates telegram profile with passed chat ID.
        """

        user = UserRepository().get_or_create(name=nickname)
        self.repository.bind_user(chat_id=chat_id, user=user)

    def find_by_chat_id(self, chat_id: int) -> TelegramProfile:
        """
        Finds telegram profile via its chat ID.

        :raises TelegramProfileNotFound: when telegram profile not found.
        """

        return self.repository.find_by_chat_id(chat_id=chat_id)
