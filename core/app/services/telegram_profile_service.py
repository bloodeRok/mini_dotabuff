from core.app.repositories import UserRepository, TelegramProfileRepository
from core.models import TelegramProfile


class TelegramProfileService:
    repository = TelegramProfileRepository()

    def get_or_create(self, chat_id: int, nickname: str) -> TelegramProfile:
        """
        Creates telegram profile with passed chat ID.
        """

        user = UserRepository().get_or_create(name=nickname)
        return self.repository.get_or_create(chat_id=chat_id, user=user)
