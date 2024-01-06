import argparse
from dotenv import load_dotenv
import os
from loguru import logger
import requests
from requests.exceptions import ConnectionError
import telegram
from time import sleep

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DEVMAN_API_TOKEN = os.getenv('DEVMAN_API_TOKEN')

parser = argparse.ArgumentParser(
    description='Программа отправляет уведомления о проверке работ преподавателем в указанный чат'
)
parser.add_argument('chat_id', help='Идентификатор пользователя телеграм')
args = parser.parse_args()


bot = telegram.Bot(token=BOT_TOKEN)


def send_request(timestamp=None):
    headers = {
        "Authorization": f"Token {DEVMAN_API_TOKEN}"
    }
    try:
        if timestamp:
            url = f"https://dvmn.org/api/long_polling/?timestamp={timestamp}"
        else:
            url = f"https://dvmn.org/api/long_polling/"
        response = requests.get(url, headers=headers, timeout=100).json()
        if response:
            if response['status'] == "found":
                send_notify(response)
        return response
    except requests.exceptions.Timeout as err:
        logger.error("Timeout occurred: {}".format(err))
    except ConnectionError:
        logger.error("Connection error")


def send_notify(response):
    if response['new_attempts']:
        message = ""
        for new_attempt in response['new_attempts']:
            message += f"Преподаватель проверил работу: \"{new_attempt['lesson_title']}\" {new_attempt['lesson_url']}\n"
            if new_attempt['is_negative']:
                message += "К сожалению, в работе нашлись ошибки \n"
            else:
                message += "Преподавателю все понравилось, можно приступать к следующему уроку!"
            bot.send_message(text=message, chat_id=args.chat_id)


def main():
    logger.info('Work started')
    while True:
        response = send_request()
        if response:
            if response["status"] == "timeout":
                timestamp = response["timestamp_to_request"]
                send_request(timestamp)
        sleep(5)


if __name__ == '__main__':
    main()
