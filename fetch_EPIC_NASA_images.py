from posting_images_in_telegram import save_image
from dotenv import load_dotenv
from posting_images_in_telegram import requests
import os
import argparse
import datetime
from telegram_bot_space import prepare_directory

def parse_and_validate_args():
    parser = argparse.ArgumentParser(
        description='Программа сохраняет указанное количество картинок EPIC NASA на текущую дату'
    )
    parser.add_argument('--max_images', help='Количество картинок EPIC NASA на текущую дату', type=int)
    args = parser.parse_args()

    if args.max_images is None:
        print('Вы сохраняете все картинки EPIC NASA на текущую дату')
    else:
        print(f'Вы сохраняете {args.max_images} картинки EPIC NASA на текущую дату')
    return args


def get_nasa_epic_url(api_key):
    base_url = 'https://epic.gsfc.nasa.gov/api/natural'
    params = {'api_key': api_key}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json()


def prepare_image_payload(data):
    image_names = [item['image'] for item in data]
    image_date = data[0]['date']
    date_obj = datetime.datetime.strptime(image_date, "%Y-%m-%d %H:%M:%S")
    payload = {
        'year': date_obj.year,
        'month': f"{date_obj.month:02d}",
        'day': f"{date_obj.day:02d}"
    }
    return image_names, payload


def save_images(directory_path, payload, image_names, api_key, max_images):
    request_params = {"api_key": api_key}
    for index, image_name in enumerate(image_names, start=1):
        link_image = (
            f'https://api.nasa.gov/EPIC/archive/natural/'
            f'{payload["year"]}/{payload["month"]}/{payload["day"]}/png/{image_name}.png'
        )
        response = requests.get(link_image, params=request_params)
        response.raise_for_status()
        filename = directory_path / f'EPIC_{index}.png'
        save_image(filename, response.url)
        if max_images is not None and index >= max_images:
            break


def fetch_and_save_epic_images(api_key, args):
    data = get_nasa_epic_url(api_key)
    image_names, payload = prepare_image_payload (data)
    directory_path = prepare_directory('images')
    save_images(directory_path, payload, image_names, api_key, args.max_images)
    print("Все изображения успешно сохранены!")


def main():
    args = parse_and_validate_args()
    load_dotenv()
    api_key = os.environ['NASA_API_KEY']
    if not api_key:
        raise ValueError("API ключ NASA не найден. Убедитесь, что переменная API_NASA установлена в .env файле.")
    fetch_and_save_epic_images(api_key, args)


if __name__ == '__main__':
    main()