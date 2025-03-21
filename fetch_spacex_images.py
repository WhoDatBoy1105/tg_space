from main import save_image
from main import requests
from pathlib import Path
from main import argparse
from urllib.parse import urlencode


def parse_and_validate_args():
    parser = argparse.ArgumentParser(
        description='Программа сохраняет картинки по id запуска SpaceX, без указания скачивает с последнего запуска'
    )
    parser.add_argument('--id_spacex', help='ID запуска SpaceX', type=str)
    args = parser.parse_args()

    if args.id_spacex is None:
        print('Вы сохраняете фото последнего запуска SpaceX, если они есть')
    else:
        print(f'Вы сохраняете фото последнего запуска SpaceX, по ID {args.id_spacex}')

    return args


def get_spacex_url(args):
    base_url = 'https://api.spacexdata.com/v5/launches'
    if args.id_spacex is None:
        return f'{base_url}/latest'
    return f'{base_url}/{args.id_spacex}'


def fetch_spacex_data(url):
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    image_urls = data['links']['flickr']['original']
    if not image_urls:
        raise ValueError("Для указанного запуска нет доступных изображений.")
    return image_urls


def prepare_directory(path=None):
    if path is None:
        directory_path = Path(__file__).parent / 'images'
    else:
        directory_path = Path(path)
    directory_path.mkdir(parents=True, exist_ok=True)
    return directory_path


def save_images(directory_path, image_urls):
    for image_number, image_url in enumerate(image_urls):
        filename = directory_path / f'spacex_{image_number}.jpg'
        save_image(filename, image_url)


def fetch_and_save_images(args):
    try:
        url = get_spacex_url(args)
        image_urls = fetch_spacex_data(url)
        directory_path = prepare_directory()
        save_images(directory_path, image_urls)

        print("Все изображения успешно сохранены!")

    except requests.exceptions.RequestException as req_err:
        print(f"Ошибка при запросе к API: {req_err}")
    except ValueError as val_err:
        print(f"Ошибка: {val_err}")
    except Exception as err:
        print(f"Произошла непредвиденная ошибка: {err}")


def main():
    args = parse_and_validate_args()
    fetch_and_save_images(args)


if __name__ == '__main__':
    main()