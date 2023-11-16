# Mini-dotabuff
Проект состоит из двух частей:
* backend часть для сохранения всех игр и работы с ними
* Telegram-бот для работы с клиентом

## Установка

### Требования
- [git](https://git-scm.com/)
- [docker](https://docs.docker.com/)
- [docker-compose](https://docs.docker.com/compose/)

### Запуск проекта
1. Клонируйте репозиторий:
`git clone https://github.com/bloodeRok/mini_dotabuff.git`.
2. Перейдите в директорию проекта: `cd "path to project"`.
3. Создайте в корневом каталоге файл .env (пример находится в .env.example) 
и заполните его.
4. Запустите проект с помощью docker-compose: `docker-compose up -d --build`.

### Документация 
Документация к проекту доступна по адресу http://127.0.0.1:1883/api/swagger.

### Работа с проектом
Для обращения к backend части используется Telegram 
(https://t.me/MiniDOTABUFF_bot). Для запуска бота потребуется нажать на 
кнопку "start" или ввести команду /start. Все дальнейшие иструкции будут в 
письме ответа.