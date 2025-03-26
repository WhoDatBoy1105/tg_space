import requests
import os.path
from urllib.parse import urlparse
from dotenv import load_dotenv
from telegram_bot_space import run_bot


def save_image(filename, image_url):
    response = requests.get(image_url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def main():
    load_dotenv()
    print("Бот запущен")
    run_bot()
    pass


if __name__ == '__main__':
    main()