CORE_URL = "http://172.18.0.3:8000"

BIND_USER_URL = CORE_URL + "/telegram-profiles/"
ADD_GAMES_URL = CORE_URL + "/telegram-profiles/{chat_id}/games/"
GET_USER_URL = CORE_URL + "/telegram-profiles/{chat_id}/user/"
SYNCHRONISE_GAMES_URL = CORE_URL \
                        + "/telegram-profiles/{chat_id}/games/synchronise/"
RETRIEVE_GAMES_URL = CORE_URL + "/telegram-profiles/{chat_id}/games/"
RETRIEVE_HEROES_URL = CORE_URL + "/heroes/"
