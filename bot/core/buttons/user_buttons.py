from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

add_user_button = InlineKeyboardButton("Add User", callback_data="add_user")

add_user_kb = InlineKeyboardMarkup()
add_user_kb.add(add_user_button)


