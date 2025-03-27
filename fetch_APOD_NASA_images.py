from posting_images_in_telegram import save_image
from posting_images_in_telegram import os
from dotenv import load_dotenv
from posting_images_in_telegram import requests
from telegram_bot_space import prepare_directory
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Программа сохраняет картинку дня APOD по выбранной дате'
    )
    parser.add_argument('--date_apod', help='Введите дату нужных фотографий APOD в формате год-месяц-день', type=str)
    return parser.parse_args()


def get_nasa_apod_data(api_key, date):
    url = 'https://api.nasa.gov/planetary/apod'
    params = {'api_key': api_key, 'date': date}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def save_nasa_image(directory_path, date, image_url):
    filename = directory_path / f'nasa_apod_{date}.jpg'
    save_image(filename, image_url)
    print(f"Изображение успешно сохранено: {filename}")


def fetch_and_save_apod_image(api_key, date):
    data = get_nasa_apod_data(api_key, date)
    image_url = data.get('url')
    directory_path = prepare_directory('images')
    save_nasa_image(directory_path, date or "today", image_url)


def main():
    args = parse_arguments()
    load_dotenv()
    api_key = os.environ['NASA_API_KEY']
    if not api_key:
        raise ValueError("API ключ NASA не найден. Убедитесь, что переменная API_NASA установлена в .env файле.")
    fetch_and_save_apod_image(api_key, args.date_apod)


if __name__ == '__main__':
    main()