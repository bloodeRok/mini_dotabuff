from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from bot.core import dp
from bot.core.buttons import add_user_kb
from bot.core.repositories import UserRepository
from bot.core.states import UserStates


@dp.message_handler(commands=["get_user"], state="*")
async def get_user(message: Message, state: FSMContext):
    user_repository = UserRepository()
    await UserStates.get_user.set()
    res = await user_repository.get_user(name="bloodeR")
    await message.reply(
        f"name : {res.get('name')}\n"
        f"matches_recorded : {res.get('matches_recorded')}\n"
        f"win_rate : {res.get('win_rate')}\n"
        f"favorite_hero : {res.get('favorite_hero')}\n"
        f"avg_gpm : {res.get('avg_gpm')}\n"
        f"avg_xpm : {res.get('avg_xpm')}\n"
        f"avg_kda : {res.get('avg_kda')}\n",
        reply_markup=add_user_kb
    )
