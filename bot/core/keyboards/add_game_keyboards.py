from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

# 404 status code
not_found_add_game_buttons = [
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

not_found_add_game_kb = InlineKeyboardMarkup(
    inline_keyboard=not_found_add_game_buttons
)
