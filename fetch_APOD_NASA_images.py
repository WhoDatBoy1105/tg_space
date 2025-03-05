from main import*
import datetime

def image_nasa():
    date_apod = str(input('Введите дату нужных фотографий APOD в формате год-месяц-день: '))
    url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': API_NASA,
        'date' : date_apod,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    nasa_images = data.get('url')
    directory_path = pathlib.Path(f'C:/Users/PC/Desktop/tg_space/images')
    directory_path.mkdir(parents=True, exist_ok=True)
    filename = directory_path / f'nasa_images.jpg'
    save_image(filename, nasa_images)

if __name__ == '__main__':
    image_nasa()