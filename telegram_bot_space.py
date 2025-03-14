from main import telegram
from main import threading
from main import os
from main import random
from main import Path


def bot_send_message():
    threading.Timer(14400, bot_send_message).start()
    path_to_images = Path(r'\Users\PC\Desktop\tg_space\images')
    images = os.listdir(path_to_images)
    img_path = random.choice(images)
    image_send = os.path.join(path_to_images, img_path)
    with open(image_send, 'rb') as photo_file:
        bot.send_photo(chat_id= CHAT_ID, photo=photo_file)

if __name__ == '__main__':
    API_TElEGRAM = os.getenv('API_TElEGRAM')
    CHAT_ID = os.getenv('CHAT_ID')
    bot = telegram.Bot(API_TElEGRAM)
    bot_send_message()