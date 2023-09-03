from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

to_admin__button = [
    [
        InlineKeyboardButton(
            text="Написать админу",
            url="t.me/spoluyakhtov"
        )
    ]
]

to_admin__kb =  InlineKeyboardMarkup(
    inline_keyboard=to_admin__button
)
