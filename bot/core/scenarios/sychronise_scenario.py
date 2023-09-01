from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.core.keyboards import (
    to_admin__kb,
)
from bot.core.repositories import UserRepository
from ..constants.sticker_constants import DOWNLOAD
from ..utils.bot_init import bot


async def synchronise_games(message: Message, state: FSMContext):
    chat_id = message.chat.id

    download_messages = [
        await bot.send_message(
            chat_id=chat_id,
            text="Идёт процесс синхронизации... Подождите."
        ),
        await bot.send_sticker(
            chat_id=chat_id,
            sticker=DOWNLOAD
        )
    ]

    res_code, detail = await UserRepository().synchronise_games(
        chat_id=chat_id,
    )

    for message in download_messages:
        await message.delete()

    match res_code:
        case 201:
            await message.answer(
                f"Игры успешно синхронизованы!"
            )

        case 404:
            await message.answer(detail)

        case 500:
            await message.answer(
                "Что-то пошло не так!",
                reply_markup=to_admin__kb
            )

    await state.clear()
