from main import*

def image_nasa_epic():
    url = 'https://epic.gsfc.nasa.gov/api/natural'
    params = {
        'images' : '',
        'api_key': API_NASA
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
        link_image.append(f'https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name[i]}.png?api_key={API_NASA}')
    directory_path = pathlib.Path(f'C:/Users/PC/Desktop/tg_space/images')
    directory_path.mkdir(parents=True, exist_ok=True)
    for image_number, image_url in enumerate(link_image):
        filename = directory_path / f'EPIC_{image_number}.jpg'
        save_image(filename, image_url)

if __name__ == '__main__':
    image_nasa_epic()