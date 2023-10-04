import requests
import telegram
import time
from requests.exceptions import Timeout, ConnectionError
from environs import Env


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
    DEVMAN_TOKEN = env('DEVMAN_TOKEN')
    BOT_TOKEN = env('BOT_TOKEN')
    CHAT_ID = env('CHAT_ID')

    timestamp = None
    bot = telegram.Bot(token=BOT_TOKEN)
    while True:
        try:
            response = get_dvmn_response(timestamp, DEVMAN_TOKEN)
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
                    chat_id=CHAT_ID,
                    text=f"Урок [{lesson_title}]({lesson_url}) проверен.\n" \
                         f'{result}'
                )
        except Timeout:
            pass
        except ConnectionError:
            time.sleep(3)
    

if __name__ == '__main__':
    main()
