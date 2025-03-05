import requests
import pathlib
import datetime
import os.path
import telegram
import imghdr
from urllib.parse import urlparse
from dotenv import load_dotenv
from datetime import datetime
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

load_dotenv()
API_NASA = os.getenv('API_NASA')
API_TElEGRAM = os.getenv('API_TElEGRAM')

def file_extension(image_url):
    parce = urlparse(image_url)
    print((os.path.splitext(parce.path))[-1])

def save_image(filename, image_url):
    response = requests.get(image_url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)
    print(f"Изображение сохранено: {filename}")

def main():
    pass


if __name__ == '__main__':
    main()