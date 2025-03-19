from main import save_image
from main import os
from dotenv import load_dotenv
from main import requests
from pathlib import Path
from main import argparse
from urllib.parse import urlencode


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Программа сохраняет картинку дня APOD по выбранной дате'
    )
    parser.add_argument('--date_apod', help='Введите дату нужных фотографий APOD в формате год-месяц-день', type=str)
    return parser.parse_args()


def handle_date_argument(args):
    if args.date_apod is None:
        print('Вы сохраняете фото APOD на сегодняшний день')
        return "today"
    print(f'Вы сохраняете фото APOD за {args.date_apod}')
    return args.date_apod


def get_nasa_apod_data(api_key, date):
    url = 'https://api.nasa.gov/planetary/apod'
    params = {'api_key': api_key, 'date': date}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def prepare_directory(path=None):
    directory_path = Path(__file__).parent / 'images' if path is None else Path(path)
    directory_path.mkdir(parents=True, exist_ok=True)
    return directory_path


def save_nasa_image(directory_path, date, image_url):
    filename = directory_path / f'nasa_apod_{date}.jpg'
    save_image(filename, image_url)
    print(f"Изображение успешно сохранено: {filename}")


def fetch_and_save_apod_image(api_key, date):
    try:
        data = get_nasa_apod_data(api_key, date)
        media_type = data.get('media_type')
        if media_type == 'image':
            image_url = data.get('url')
        elif media_type == 'video':
            print("APOD за выбранную дату является видео. Сохранение изображений невозможно.")
            return
        else:
            print(f"Неизвестный тип медиа: {media_type}")
            return
        directory_path = prepare_directory()
        save_nasa_image(directory_path, date or "today", image_url)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")


def main():
    args = parse_arguments()
    date = handle_date_argument(args)
    load_dotenv()
    api_key = os.getenv('NASA_API_KEY')
    if not api_key:
        raise ValueError("API ключ NASA не найден. Убедитесь, что переменная API_NASA установлена в .env файле.")
    fetch_and_save_apod_image(api_key, args.date_apod)


if __name__ == '__main__':
    main()