import os
import random
import threading
from pathlib import Path
from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackContext


def prepare_directory(path=None):
    directory_path = Path(__file__).parent / 'images' if path is None else Path(path)
    directory_path.mkdir(parents=True, exist_ok=True)
    return directory_path


def get_random_image(path_to_images):
    images = [file for file in os.listdir(path_to_images) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not images:
        raise FileNotFoundError("В директории нет изображений.")
    return Path(path_to_images) / random.choice(images)


def send_random_image(bot, chat_id, path_to_images):
    image_path = get_random_image(path_to_images)
    print(f"Выбранное изображение: {image_path}")
    with open(image_path, 'rb') as photo_file:
        bot.send_photo(chat_id=chat_id, photo=photo_file)
    print(f"Изображение успешно отправлено: {image_path}")



def start_bot(update, context):
    update.message.reply_text("Привет! Я бот, который отправляет случайные изображения из космоса!")


def send_image_periodically(bot, chat_id, path_to_images):
    threading.Timer(14400, send_image_periodically, args=(bot, chat_id, path_to_images)).start()
    send_random_image(bot, chat_id, path_to_images)


def run_bot():
    TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
    TG_CHAT_ID = os.getenv('TG_CHAT_ID')
    path_to_images = prepare_directory()
    bot = Bot(token=TELEGRAM_API_KEY)
    updater = Updater(token=TELEGRAM_API_KEY, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_bot))
    send_image_periodically(bot, TG_CHAT_ID, path_to_images)
    updater.start_polling()
    updater.idle()