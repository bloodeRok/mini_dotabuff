from enum import Enum


class RetrieveGamesButtons(Enum):
    last_days = "по последним дням"
    hero = "по герою"
    top = "по количеству"
    interval = "по интервалу дат"
    over_filterring = "отправить запрос"
    all_games = "просто все игры"
