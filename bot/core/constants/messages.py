WELCOME_MESSAGE = """
Привет! Я бот по отслеживанию игр и высчитыванию твоей статистики\n
Я могу показывать твои игры: /retrieve_games\n
Показывать краткую статистику: /get_stats\n

Чтобы начать работу:
1) Привяжите Ваш аккаунт DOTA 2 (/bind)\n
2) Добавьте игры (/add_games)\n
3) Если Вы сыграли игры и хотите добавить последние матчи, то синхронизуйте
матчи (/synchronise)

Если потребуется помощь - /help

Если вопрос странный и нерешаемый, то пишите мне:
"""

START_BIND_MESSAGE =  """
Давай привяжем этот чат к игроку\n 
Напиши ниже DOTA ID
"""

START_ADD_GAME_MESSAGE =  """
Давай привяжем к твоему аккаунту игры\n 
Сколько последних игр ты бы хотел привязать?\n\n
P.S. Привязать можно максимум 50 игр.
"""

START_RETRIEVE_GAMES_MESSAGE = """
Сейчас выведу тебе игры!\n
По каким параметрам их отфильтровать?
"""

HELP_MESSAGE = """
Бот хранит твои игры и выводит по ним статистику. Основные комманды бота:\n
/bind - привязать аккаунт телеграмма к аккаунту доты\n
/add_games - загрузить последние игры (требуется, когда игр к аккаунт ещё не привязано)\n
/synchronise - синхронизовать игры (добавить последние игры к уже существующим)\n
/get_stats - получить краткую статистику\n
/retrieve_games - вывести последние игры списком (используя фильтры)
"""