from main import save_image
from main import requests
from main import pathlib
from main import argparse


def fetch_spacex_last_launch():
    parser = argparse.ArgumentParser(
        description='Программа сохраняет картинки по id запуска SpaceX, без указания скачивает с последнего запуска')
    parser.add_argument('--id_spacex', help='id запуска SpaceX', type=str)
    args = parser.parse_args()
    if args.id_spacex is None:
        url = 'https://api.spacexdata.com/v5/launches/latest'
        print('Вы сохраняете фото последнего запуска spaceX, если они есть')
    else:
        url = f'https://api.spacexdata.com/v5/launches/{args.id_spacex}'
        print(f'Вы сохраняете фото последнего запуска spaceX, по id {args.id_spacex}')
    response = requests.get(url)
    response.raise_for_status()
    original_images = response.json()['links']['flickr']['original']
    directory_path = pathlib.Path(f'C:/Users/PC/Desktop/tg_space/images')
    directory_path.mkdir(parents=True, exist_ok=True)
    for image_number, image_url in enumerate(original_images):
        filename = directory_path / f'spacex_{image_number}.jpg'
        save_image(filename, image_url)


if __name__ == '__main__':
    fetch_spacex_last_launch()