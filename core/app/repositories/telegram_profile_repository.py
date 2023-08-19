from core.models import User, TelegramProfile


class TelegramProfileRepository:
    model = TelegramProfile

    def get_or_create(self, chat_id: int, user: User) -> TelegramProfile:
        """
        Creates telegram profile with passed chat ID or creates one.
        """

        tg_profile = self.model.objects.filter(chat_id=chat_id).first()
        if not tg_profile:
            tg_profile = self.model.objects.create(chat_id=chat_id, user=user)
        return tg_profile
