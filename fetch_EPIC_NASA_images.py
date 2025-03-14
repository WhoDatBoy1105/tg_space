from main import save_image
from dotenv import load_dotenv
from main import os
from main import datetime
from main import requests
from main import pathlib


def save_image_nasa_epic():
    load_dotenv()
    API_NASA = os.getenv('API_NASA')
    url = 'https://epic.gsfc.nasa.gov/api/natural'
    params = {
        'api_key': API_NASA
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    image_name = []
    for item in data:
         image_name.append(item['image'])
         image_date = item['date']

    date_obj = datetime.strptime(image_date, "%Y-%m-%d %H:%M:%S")
    payload = {
        'year': date_obj.year,
        'month': "{:02d}".format(date_obj.month),
        'day': "{:02d}".format(date_obj.day)
    }

    directory_path = pathlib.Path(f'C:/Users/PC/Desktop/tg_space/images')
    directory_path.mkdir(parents=True, exist_ok=True)

    for i in range (5):
        link_image = (
            f'https://api.nasa.gov/EPIC/archive/natural/'
            f'{payload["year"]}/{payload["month"]}/{payload["day"]}/png/{image_name[i]}.png?api_key={API_NASA}'
        )
        filename = directory_path / f'EPIC_{i + 1}.png'
        save_image(filename, link_image)

if __name__ == '__main__':
    save_image_nasa_epic()