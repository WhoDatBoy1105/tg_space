import requests
import os
import argparse
import datetime
from pathlib import Path
from posting_images_in_telegram import save_image
from dotenv import load_dotenv


def parse_args():
    parser = argparse.ArgumentParser(
        description='Сохраняет указанное количество EPIC-изображений NASA за текущую дату.'
    )
    parser.add_argument('--count', type=int, help='Количество изображений для сохранения')
    args = parser.parse_args()

    if args.count is None:
        print('Будут сохранены все доступные EPIC-изображения NASA.')
    else:
        print(f'Будет сохранено {args.count} EPIC-изображений NASA.')
    return args


def fetch_epic_data(api_key):
    url = 'https://epic.gsfc.nasa.gov/api/natural'
    response = requests.get(url, params={'api_key': api_key})
    response.raise_for_status()
    return response.json()


def extract_image_info(data):
    image_names = [item['image'] for item in data]
    date_obj = datetime.datetime.strptime(data[0]['date'], "%Y-%m-%d %H:%M:%S")
    date_parts = {
        'year': date_obj.year,
        'month': f"{date_obj.month:02d}",
        'day': f"{date_obj.day:02d}"
    }
    return image_names, date_parts


def build_image_url(date_parts, image_name, api_key):
    url = (
        f'https://api.nasa.gov/EPIC/archive/natural/'
        f'{date_parts["year"]}/{date_parts["month"]}/{date_parts["day"]}/png/{image_name}.png'
    )
    return url


def download_image(url, api_key):
    params = {"api_key": api_key}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response


def save_single_image(directory, index, image_response):
    file_path = directory / f'EPIC_{index}.png'
    save_image(file_path, image_response.url)


def save_images(directory, date_parts, image_names, api_key, max_count):
    for index, name in enumerate(image_names, start=1):
        url = build_image_url(date_parts, name, api_key)
        image_response = download_image(url, api_key)
        save_single_image(directory, index, image_response)

        if max_count and index >= max_count:
            break


def download_epic_images(api_key, max_count, directory):
    directory.mkdir(parents=True, exist_ok=True)

    data = fetch_epic_data(api_key)
    image_names, date_parts = extract_image_info(data)
    save_images(directory, date_parts, image_names, api_key, max_count)
    print("Изображения успешно сохранены!")


def main():
    args = parse_args()
    load_dotenv()
    directory = Path(os.getenv('DIRECTORY_PATH', './images'))
    api_key = os.environ.get('NASA_API_KEY')
    if not api_key:
        raise ValueError("API ключ NASA не найден. Убедитесь, что переменная NASA_API_KEY установлена в .env файле.")
    download_epic_images(api_key, args.count, directory)


if __name__ == '__main__':
    main()