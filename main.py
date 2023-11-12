import requests
import telegram
import time
import logging
from logging.handlers import SysLogHandler
from requests.exceptions import Timeout, ConnectionError
from environs import Env


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
syslog_handler = SysLogHandler(address='/dev/log')
syslog_handler.setLevel(logging.INFO)
logger.addHandler(syslog_handler)


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

    while True:
        try:
            bot = telegram.Bot(token=tg_bot_token)
            bot_info = bot.getMe()
            logger.info('Bot started')
            break
        except telegram.TelegramError:
            logger.error('Error connecting to Telegram bot.')

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
        except Timeout:
            pass
        except ConnectionError:
            time.sleep(3)
    

if __name__ == '__main__':
    main()
