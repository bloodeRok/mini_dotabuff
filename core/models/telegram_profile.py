from django.db import models

from core.constants.field_restrictions import NAME_MAX_LENGTH


class TelegramProfile(models.Model):
    chat_id = models.IntegerField(
        help_text="Chat ID of the user.",
        unique=True
    )
    

    #  Relationships.
    user = models.ForeignKey(
        "User",
        on_delete=models.PROTECT,
        related_name="chat_ids"
    )

    def __repr__(self):
        return f"<TelegramProfile(" \
               f"pk={self.pk}, " \
               f"chat_id={self.chat_id} " \
               f")>"

    def __str__(self):
        return self.__repr__()
