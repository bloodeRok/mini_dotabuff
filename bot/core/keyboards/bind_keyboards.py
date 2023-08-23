from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# to information
bind_game__where_dotabuff_id__button = [
    [
        InlineKeyboardButton(
            text="Я не знаю, где взять этот ваш \"ID дотабаффа\"",
            callback_data="where_dotabuff_player_id"
        )
    ]
]

bind_game__where_dotabuff_id__kb =  InlineKeyboardMarkup(
    inline_keyboard=bind_game__where_dotabuff_id__button
)

# To dotabuff site
bind_game__how_to_find__button = [
    [
        InlineKeyboardButton(
            text="Ссылка на dotabuff",
            url="https://www.dotabuff.com/"
        )
    ]
]

bind_game__how_to_find__kb = InlineKeyboardMarkup(
    inline_keyboard=bind_game__how_to_find__button
)
