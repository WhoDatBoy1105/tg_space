from main import save_image
from dotenv import load_dotenv
from main import os
from main import datetime
from main import requests
from pathlib import Path
from urllib.parse import urlencode


def load_nasa_api_key():
    load_dotenv()
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


def save_images(directory_path, payload, image_names, api_key):
    max_images = min(len(image_names), 5)
    for i in range(max_images):
        link_image = (
            f'https://api.nasa.gov/EPIC/archive/natural/'
            f'{payload["year"]}/{payload["month"]}/{payload["day"]}/png/{image_names[i]}.png?{urlencode({"api_key": api_key})}'
        )
        filename = directory_path / f'EPIC_{i + 1}.png'
        save_image(filename, link_image)


def fetch_and_save_epic_images(api_key):
    try:
        data = get_nasa_epic_url(api_key)
        image_names, payload = create_image_by_date(data)
        directory_path = prepare_directory()
        save_images(directory_path, payload, image_names, api_key)
        print("Все изображения успешно сохранены!")
    except requests.exceptions.RequestException as req_err:
        print(f"Ошибка при запросе к API: {req_err}")
    except ValueError as val_err:
        print(f"Ошибка: {val_err}")
    except Exception as err:
        print(f"Произошла непредвиденная ошибка: {err}")


def main():
    try:
        api_key = load_nasa_api_key()
        fetch_and_save_epic_images(api_key)
    except Exception as err:
        print(f"Произошла ошибка: {err}")


if __name__ == '__main__':
    main()