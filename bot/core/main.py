from aiogram.utils import executor

from bot.core.app import dp

if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True)