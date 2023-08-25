from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
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

# input count of games
add_games__count__buttons = [
    [
        KeyboardButton(
            text="5"
        ),
        KeyboardButton(
            text="10",
        )
    ],
    [
        KeyboardButton(
            text="20",
        ),
        KeyboardButton(
            text="30",
        )
    ],
    [
        KeyboardButton(
            text="40",
        ),
        KeyboardButton(
            text="50",
        )
    ],
    [
        KeyboardButton(
            text="Сам введу",
        )
    ]
]

add_game__count__kb = ReplyKeyboardMarkup(
    keyboard=add_games__count__buttons,
    resize_keyboard=True,
    one_time_keyboard=True
)
