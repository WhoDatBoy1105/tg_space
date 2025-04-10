# Загрузка фотографий NASA

Проект служит для загрузки фотографий NASA и Starlink за последний период

### Как установить
* Настройте окружения перед запуском программы
* Переменные окружения: 
1. NASA_API_KEY - сервисный токен для авторизации API NASA, необходим для работы с фотографиями на сайте NASA
2. TELEGRAM_API_KEY - сервисный токен для авторизации Telegram, необходим для работы с мессенджером Telegram
3. TG_CHAT_ID - ID пользователя или чата в Telegram, на который будут приходить фотографии
4. DIRECTORY_PATH - путь к файлам с которых будет происходить загрузка изображений
5. POST_FREQUENCY - таймер цикла отправки изображений в телеграм
#### Инструкция по получению сервисного токена VK

* [Получите сервисный токен NASA](https://api.nasa.gov/n)

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
---
### Примеры запуска скрипта `fetch_spacex_images.py`
#### При запуске без указания id полета

**Пример вывода:**
```
Вы сохраняете фото последнего запуска spaceX, если они есть

Process finished with exit code 0
....
```
#### При запуске с указанием id полета
**Пример запуска:**
```bash
* python fetch_spacex_images.py --spacex_id 5eb87d42ffd86e000604b384
```
**Пример вывода:**
```
Вы сохраняете фото последнего запуска spaceX, по id 5eb87d42ffd86e000604b384
Изображение сохранено: ...\images\spacex_0.jpg
```
### Примеры запуска скрипта `fetch_APOD_NASA_images.py`
#### При запуске без указания даты
**Пример вывода:**
```
Вы сохраняете фото APOD на сегодняшний день
Изображение успешно сохранено: ...\images\nasa_apod_today.jpg
```
#### При запуске с указанием даты
**Пример запуска:**
```bash
* python fetch_APOD_NASA_images.py --date_apod 2013-11-22 
```
**Пример вывода:**

```
Вы сохраняете фото APOD за 2013-11-22
Изображение успешно сохранено: ...\images\nasa_apod_2013-11-22.jpg
```
### Примеры запуска скрипта `fetch_EPIC_NASA_images.py`
#### При запуске без указания количества изображений
**Пример вывода:**
```
Вы сохраняете все картинки EPIC NASA на текущую дату
Изображение сохранено: ...\images\EPIC_1.png
Изображение сохранено: ...\images\EPIC_2.png
...
```
#### При запуске с указанием количества изображений
**Пример запуска:**
```bash
* python fetch_EPIC_NASA_images.py --max_images 2 
```
**Пример вывода:**

```
Вы сохраняете 2 картинки EPIC NASA на текущую дату
Изображение сохранено: ...\images\EPIC_1.png
Изображение сохранено: ...\images\EPIC_2.png
```
### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
 
