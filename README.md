# devman_notofication_bot
Бот, который отправляет уведомление в telegram указанному при запуске скрипта пользователю, когда работа пройдет проверку преподавателем.

## Запуск
- BOT_TOKEN - Токен бота токен бота, полученный в BotFather. Должен быть указан в файле .env
- DEVMAN_API_TOKEN - Token api devman, полученный в личном кабинете devman, на странице https://dvmn.org/api/docs/. Должен быть указан в файле .env
- Идентификаор пользователя telegram передается при запуске скрипта


Скопируйте `.env.example` в `.env` и отредактируйте `.env` файл, заполнив в нём все переменные окружения:
```bash
cp devman_notofication_bot/.env.example devman_notofication_bot/.env
```

Для управления зависимостями используется [pip](https://pip.pypa.io/en/stable/),
требуется Python 3.8.

Установка зависимостей и запуск бота:

```bash
pip install -r requirements.txt
python python main.py {chat_id}
```
Чтобы получить свой chat_id, напишите в Telegram специальному боту: @userinfobot
