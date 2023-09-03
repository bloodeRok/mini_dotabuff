from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)

# Input count of games
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


# Redirect from adding to synchronise
add_games__from_add_to_synchronise___buttons = [
    [
        InlineKeyboardButton(
            text="Да",
            callback_data="from_add_to_synchronise"
        )
    ],
    [
        InlineKeyboardButton(
            text="Нет",
            callback_data="state_clear"
        )
    ]
]

add_games__from_add_to_synchronise__kb = InlineKeyboardMarkup(
    inline_keyboard=add_games__from_add_to_synchronise___buttons
)
