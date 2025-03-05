from main import*


def fetch_spacex_last_launch():
    id = input('Введите id для получения нужных фотографий: ')
    if id == "":
        url = 'https://api.spacexdata.com/v5/launches/latest'
    else:
        url = f'https://api.spacexdata.com/v5/launches/{id}'
    response = requests.get(url)
    response.raise_for_status()
    json_data = response.json()
    original_images = json_data['links']['flickr']['original']
    directory_path = pathlib.Path(f'C:/Users/PC/Desktop/tg_space/images')
    directory_path.mkdir(parents=True, exist_ok=True)
    for image_number, image_url in enumerate(original_images):
        filename = directory_path / f'spacex_{image_number}.jpg'
        save_image(filename, image_url)

if __name__ == '__main__':
    fetch_spacex_last_launch()