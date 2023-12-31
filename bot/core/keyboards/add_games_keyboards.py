from aiogram.types import (
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
add_games__from_add_to_synchronise__buttons = [
    [
        KeyboardButton(
            text="Да"
        )
    ],
    [
        KeyboardButton(
            text="Нет"
        )
    ]
]

add_games__from_add_to_synchronise__kb = ReplyKeyboardMarkup(
    keyboard=add_games__from_add_to_synchronise__buttons,
    resize_keyboard=True
)
