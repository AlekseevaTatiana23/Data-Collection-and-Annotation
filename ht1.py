# Напишите сценарий на языке Python, который предложит
# пользователю ввести интересующую его категорию(например, кофейни, музеи, парки
# и т.д.). Используйте API Foursquare для поиска заведений в указанной
# категории. Получите название заведения, его адрес и рейтинг
# для каждого из них. Скрипт должен вывести название и адрес
# и рейтинг каждого заведения в консоль.

import requests
import json

import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

api_key = os.getenv('API_KEY')
url = 'https://api.foursquare.com/v3/places/search'

city = input("Введите название города: ")
category = input("Введите категорию (cafe, fitness, memorial & etc): ")

params = {
    'near': city,
    'limit': 5,
    'query': category,
    'fields': 'name,location,rating'
}

headers = {
    'Accept': 'application/json',
    'Authorization': api_key
}

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    data = json.loads(response.text)
    for place in data['results']:
        print("\nНазвание:", place.get('name'))
        print("Адрес:", place.get('location').get('formatted_address'))
        print("Рейтинг:", place.get('rating', 'не определился'))
else:
    print("Запрос API завершился неудачей с кодом состояния:", response.status_code)
    print(response.text)