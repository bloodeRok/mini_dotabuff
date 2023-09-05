from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


# Redirect from synchronise to adding
synchronise__from_synchronise_to_add__buttons = [
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

synchronise__from_synchronise_to_add__kb = ReplyKeyboardMarkup(
    keyboard=synchronise__from_synchronise_to_add__buttons,
    resize_keyboard=True
)