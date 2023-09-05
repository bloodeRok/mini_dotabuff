from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# to information
bind_game__where_dota_id__buttons = [
    [
        InlineKeyboardButton(
            text="Узнать \"DOTA ID\" через DotaBuff",
            callback_data="where_dota_player_id_dotabuff"
        )
    ],
    [
        InlineKeyboardButton(
            text="Узнать \"DOTA ID\" через клиент Dota 2",
            callback_data="where_dota_player_id_dota_client"
        )
    ]
]

bind_game__where_dota_id__kb = InlineKeyboardMarkup(
    inline_keyboard=bind_game__where_dota_id__buttons
)
