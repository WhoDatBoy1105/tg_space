from main import os
from dotenv import load_dotenv
from main import requests
from pathlib import Path
from main import argparse


def save_image(filename, image_url):
    response = requests.get(image_url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def save_image_nasa():
    parser = argparse.ArgumentParser(
        description='Программа сохраняет картинку дня APOD по выбранной дате'
    )
    parser.add_argument('--date_apod', help='Введите дату нужных фотографий APOD в формате год-месяц-день', type=str)
    args = parser.parse_args()

    if args.date_apod is None:
        print('Вы сохраняете фото APOD на сегодняшний день')
    else:
        print(f'Вы сохраняете фото APOD за {args.date_apod}')

    load_dotenv()
    API_NASA = os.getenv('API_NASA')
    if not API_NASA:
        raise ValueError("API ключ NASA не найден. Убедитесь, что переменная API_NASA установлена в .env файле.")

    params = {
        'api_key': API_NASA,
        'date': args.date_apod,
    }
    url = 'https://api.nasa.gov/planetary/apod'

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        media_type = data.get('media_type')
        if media_type == 'image':
            nasa_images = data.get('url')
        elif media_type == 'video':
            print("APOD за выбранную дату является видео. Сохранение изображений невозможно.")
            return
        else:
            print(f"Неизвестный тип медиа: {media_type}")
            return

        directory_path = Path(f'C:/Users/PC/Desktop/tg_space/images')
        directory_path.mkdir(parents=True, exist_ok=True)
        filename = directory_path / f'nasa_apod_{args.date_apod or "today"}.jpg'
        save_image(filename, nasa_images)
        print(f"Изображение успешно сохранено: {filename}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")


if __name__ == '__main__':
    save_image_nasa()