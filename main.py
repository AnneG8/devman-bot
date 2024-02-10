import time
import logging
import logging.handlers

import telegram
import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError
from environs import Env


logger = logging.getLogger(__name__)


class BotLogsHandler(logging.Handler):
    def __init__(self, bot_token, chat_id):
        super().__init__()
        self.bot = telegram.Bot(token=bot_token)
        self.chat_id = chat_id
    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id,
                              text=log_entry)


def get_dvmn_response(timestamp, token):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {token}'
    }
    payload = {
        "timestamp": timestamp
    }
    response = requests.get(url, headers=headers, params=payload, timeout=30)
    response.raise_for_status()
    return response


def main():
    env = Env()
    env.read_env()
    devman_token = env('DEVMAN_TOKEN')
    tg_bot_token = env('BOT_TOKEN')
    user_chat_id = env('CHAT_ID')
    admin_chat_id = env('ADMIN_CHAT_ID')

    logging.basicConfig(level=logging.INFO,
                        format="%(process)d %(levelname)s %(message)s")
    while True:
        try:
            bot = telegram.Bot(token=tg_bot_token)
            bot_info = bot.getMe()
            break
        except telegram.TelegramError:
            logger.error('Error connecting to Telegram bot.')
            time.sleep(300)

    logger.addHandler(BotLogsHandler(tg_bot_token, admin_chat_id))
    logger.info('Bot started')

    timestamp = None
    while True:
        try:
            response = get_dvmn_response(timestamp, devman_token)
            review = response.json()
            if review['status'] == 'timeout':
                timestamp = review['timestamp_to_request']
            elif review['status'] == 'found':
                timestamp = review['last_attempt_timestamp']
                lesson_title = review['new_attempts'][0]['lesson_title']
                lesson_url = review['new_attempts'][0]['lesson_url']
                is_negative = review['new_attempts'][0]['is_negative']
                result = 'Пришли правки.' if is_negative else 'Код принят.'
                bot.send_message(
                    chat_id=user_chat_id,
                    text=f"Урок [{lesson_title}]({lesson_url}) проверен.\n" \
                         f'{result}'
                )
        except HTTPError as err:
            logger.error(f'HTTPError: {err}')
        except Timeout:
            pass
        except ConnectionError as err:
            logger.error(f'ConnectionError: {err}')
            time.sleep(3)
    

if __name__ == '__main__':
    main()
