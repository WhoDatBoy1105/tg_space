from main import save_image
from dotenv import load_dotenv
from main import os
from main import datetime
from main import requests
from pathlib import Path
from main import argparse

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


def load_nasa_api_key():
    api_key = os.getenv('NASA_API_KEY')
    if not api_key:
        raise ValueError("NASA_API_KEY не найден в переменных окружения")
    return api_key


def prepare_directory(path=None):
    directory_path = Path(__file__).parent / 'images' if path is None else Path(path)
    directory_path.mkdir(parents=True, exist_ok=True)
    return directory_path


def get_nasa_epic_url(api_key):
    base_url = 'https://epic.gsfc.nasa.gov/api/natural'
    params = {'api_key': api_key}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json()


def create_image_by_date(data):
    image_names = [item['image'] for item in data]
    image_date = data[0]['date']
    date_obj = datetime.strptime(image_date, "%Y-%m-%d %H:%M:%S")
    payload = {
        'year': date_obj.year,
        'month': f"{date_obj.month:02d}",
        'day': f"{date_obj.day:02d}"
    }
    return image_names, payload


def save_images(directory_path, payload, image_names, api_key, args):
    request_params = {"api_key": api_key}
    for index, image_name in enumerate(image_names, start=1):
        link_image = (
            f'https://api.nasa.gov/EPIC/archive/natural/'
            f'{payload["year"]}/{payload["month"]}/{payload["day"]}/png/{image_name}.png'
        )
        response = requests.get(link_image, params=request_params)
        response.raise_for_status()
        filename = directory_path / f'EPIC_{index}.png'
        if args.max_images is None:
            save_image(filename, response.url)
        else:
            args.max_images >= index
            save_image(filename, response.url)
            break


def fetch_and_save_epic_images(api_key):
    args = parse_and_validate_args()
    data = get_nasa_epic_url(api_key)
    image_names, payload = create_image_by_date(data)
    directory_path = prepare_directory()
    save_images(directory_path, payload, image_names, api_key, args)
    print("Все изображения успешно сохранены!")


def main():
    load_dotenv()
    api_key = load_nasa_api_key()
    fetch_and_save_epic_images(api_key)



if __name__ == '__main__':
    main()