from main import*

def tg_space_bot():
    bot = telegram.Bot(API_TElEGRAM)
    bot.send_message(text='Hi!', chat_id='@space_test_devman')

if __name__ == '__main__':
    tg_space_bot()