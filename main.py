import requests
import pathlib
from urllib.parse import urlparse
import os.path
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY = os.getenv('API_KEY')

def fetch_spacex_last_launch():
    url = 'https://api.spacexdata.com/v5/launches/5eb87d47ffd86e000604b38a'
    response = requests.get(url)
    response.raise_for_status()
    json_data = response.json()
    original_images = json_data['links']['flickr']['original']
    directory = input("Введите имя директории для сохранения изображений: ")
    directory_path = pathlib.Path(f'C:/Users/PC/Desktop/tg_space/{directory}')
    directory_path.mkdir(parents=True, exist_ok=True)
    for image_number, image_url in enumerate(original_images):
        filename = directory_path / f'nasa_apod_{image_number}.jpg'
        save_image(filename, image_url)

def image_nasa():
    url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': API_KEY,
        'count' : 50
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    nasa_images = [item['url'] for item in data if item['media_type'] == 'image']
    directory_path = pathlib.Path(f'C:/Users/PC/Desktop/tg_space/images')
    directory_path.mkdir(parents=True, exist_ok=True)
    for image_number, image_url in enumerate(nasa_images):
        filename = directory_path / f'spacex_{image_number}.jpg'
        save_image(filename, image_url)

def image_nasa_epic():
    url = 'https://epic.gsfc.nasa.gov/api/natural'
    params = {
        'images' : '',
        'api_key': API_KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    image_name = []
    link_image = []
    for item in data:
         image_name.append(item['image'])
         image_date = item['date']
    date_obj = datetime.strptime(image_date, "%Y-%m-%d %H:%M:%S")
    year = date_obj.year
    month = f"{date_obj.month:02d}"
    day = f"{date_obj.day:02d}"
    for i in range (5):
        link_image.append(f'https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name[i]}.png?api_key={API_KEY}')
    directory_path = pathlib.Path(f'C:/Users/PC/Desktop/tg_space/images')
    directory_path.mkdir(parents=True, exist_ok=True)
    for image_number, image_url in enumerate(link_image):
        filename = directory_path / f'EPIC_{image_number}.jpg'
        save_image(filename, image_url)


def file_extension(image_url):
    parce = urlparse(image_url)
    print((os.path.splitext(parce.path))[-1])

def save_image(filename, image_url):
    response = requests.get(image_url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)
    print(f"Изображение сохранено: {filename}")

def main():
    image_nasa()
    image_nasa_epic()
if __name__ == '__main__':
    main()