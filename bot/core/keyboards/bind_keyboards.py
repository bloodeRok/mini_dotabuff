
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# to information
bind_game__where_dota_id__button = [
    [
        InlineKeyboardButton(
            text="Я не знаю, где взять этот ваш \" DOTA ID\"",
            callback_data="where_dota_player_id"
        )
    ]
]

bind_game__where_dota_id__kb =  InlineKeyboardMarkup(
    inline_keyboard=bind_game__where_dota_id__button
)
