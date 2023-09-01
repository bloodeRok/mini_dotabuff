from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_file import FSInputFile

from ..constants.bot_constants import PICTURES_PATH
from ..constants.messages import START_BIND_MESSAGE
from bot.core.keyboards import (
    bind_game__where_dota_id__kb,
    to_admin__kb,
)
from bot.core.repositories import UserRepository
from bot.core.utils.states import BindUserStates
from ..utils.bot_init import bot


async def start_bind(message: Message, state: FSMContext):
    await message.answer(
        START_BIND_MESSAGE,
        reply_markup=bind_game__where_dota_id__kb
    )
    await state.set_state(BindUserStates.dota_id)


async def bind_chat_to_dota_id(message: Message, state: FSMContext):
    try:
        if message.text == "/stop":
            await state.clear()
            return
        dota_user_id = int(message.text)
    except ValueError:
        await message.reply("ID должен иметь только цифры!")
        return

    res_code, json = await UserRepository().bind_user(
        chat_id=message.chat.id,
        dota_user_id=dota_user_id
    )
    match res_code:
        case 201:
            nickname = json["nickname"]
            await message.answer(
                f"Игрок c ником \"{nickname}\" успешно привязан!"
            )

        case 404:
            await message.answer("Я не нашёл профиль с таким ID.")

        case 500:
            await message.answer(
                "Что-то пошло не так!",
                reply_markup=to_admin__kb
            )
    await state.clear()


async def where_dota_id(call: CallbackQuery):

    # main_photo = FSInputFile(PICTURES_PATH + "\dotabuff_main.jpg")
    # await bot.send_photo(
    #     call.from_user.id,
    #     main_photo,
    #     caption="1) Нажимешь сюда\n"
    #             "(Если потребуется авторизоваться "
    #             "через steam - авторизовываешься)"
    # )
    #
    # url_photo = FSInputFile(PICTURES_PATH + r"\URL.jpg")
    # await bot.send_photo(
    #     chat_id=call.from_user.id,
    #     photo=url_photo,
    #     caption="2) Из URL'a достаёшь эти цифры."
    #             " Вставляешь их ниже в сообщение"
    # )
    """ TODO """

    await bot.send_message(chat_id=call.from_user.id, text="Чини фото!")
    await call.answer()
