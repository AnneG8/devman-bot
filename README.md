# Бот-извещатель для Devman

Бот, уведомляющий ученика Devman о проверке его работ.

### Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `main.py` и запишите туда данные переменные в таком формате: `ПЕРЕМЕННАЯ = значение`. 

- `DEVMAN_TOKEN` — API-токен [Devman](https://dvmn.org/). Инструкция [здесь](https://dvmn.org/api/docs/).
- `BOT_TOKEN` — API-токен Telegram-бота, можно получить при [регистрации](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram.html).
- `CHAT_ID` — ID чата телеграмм между учеником и ботом, получить можно у [userinfobot](https://telegram.me/userinfobot).
- `ADMIN_CHAT_ID` — ID чата телеграмм между администратором бота и ботом, администратору будут приходить уведомления о проблемах с ботом.

### Запуск

#### 1. Вариант №1 - используя docker-контейнер:

Установите [Docker](https://www.docker.com/get-started/).
Выполните команды из корня репозитория:

```bash
docker build -t devman-bot .
docker run -d --env-file .env devman-bot
```

#### 2. Вариант №2 - в ручную:

Выполните команды из корня репозитория:
```bash
pip install -r requirements.txt
python main.py
```
