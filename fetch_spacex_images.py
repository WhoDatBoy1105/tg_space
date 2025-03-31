import requests
import argparse
import os
from pathlib import Path
from posting_images_in_telegram import save_image
from dotenv import load_dotenv


def parse_and_validate_args():
    parser = argparse.ArgumentParser(
        description='Программа сохраняет картинки по id запуска SpaceX, без указания скачивает с последнего запуска'
    )
    parser.add_argument(
        '--spacex_id',
        default='latest',
        help='ID запуска SpaceX',
        type=str)
    args = parser.parse_args()

    if args.spacex_id == 'latest':
        print('Вы сохраняете фото последнего запуска SpaceX, если они есть')
    else:
        print(f'Вы сохраняете фото последнего запуска SpaceX, по ID {args.spacex_id}')

    return args


def fetch_spacex_data(url):
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    image_urls = data['links']['flickr']['original']
    if not image_urls:
        raise ValueError("Для указанного запуска нет доступных изображений.")
    return image_urls


def save_images(directory_path, image_urls):
    for image_number, image_url in enumerate(image_urls):
        filename = directory_path / f'spacex_{image_number}.jpg'  # Теперь directory_path - объект Path
        save_image(filename, image_url)


def fetch_and_save_images(spacex_id, directory_path):
    url = f'https://api.spacexdata.com/v5/launches/{spacex_id}'
    image_urls = fetch_spacex_data(url)
    save_images(directory_path, image_urls)
    print(url)
    print("Все изображения успешно сохранены!")


def main():
    load_dotenv()
    directory_path = os.getenv('DIRECTORY_PATH', './images')
    directory_path = Path(directory_path)
    args = parse_and_validate_args()
    fetch_and_save_images(args.spacex_id, directory_path)


if __name__ == '__main__':
    main()