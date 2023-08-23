from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

# 404 status code
add_game__not_found__buttons = [
    [
        InlineKeyboardButton(
            text="1) Ты ошибся с ID игры.",
            callback_data="add_game"
        )
    ],
    [
        InlineKeyboardButton(
            text="2) Ты сменил ник в игре, тут его не поменял",
            callback_data="change_nickname"
        )
    ],
    [
        InlineKeyboardButton(
            text="3) У тебя закрыт профиль на DOTABUFF.",
            url="https://www.dotabuff.com/settings"
        )
    ]
]

add_game__not_found__kb = InlineKeyboardMarkup(
    inline_keyboard=add_game__not_found__buttons
)
