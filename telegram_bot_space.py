from main import*

bot = telegram.Bot(API_TElEGRAM)

def bot_send_message():
    threading.Timer(14400, bot_send_message).start()
    path_to_images = Path(r'C:\Users\PC\Desktop\tg_space\images')
    images = os.listdir(path_to_images)
    img_path = random.choice(images)
    image_send = os.path.join(path_to_images, img_path)
    bot.send_photo(chat_id='@space_test_devman', photo=open(image_send, 'rb'))

if __name__ == '__main__':
    bot_send_message()