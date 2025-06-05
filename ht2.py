import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import pandas as pd
import urllib.parse  # Импортируем для обработки URL
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ua = UserAgent()

base_url = 'https://books.toscrape.com/' # Базовый URL для формирования абсолютных URL
url = base_url # Начальный URL
headers = {'User-Agent': ua.chrome}

session = requests.session()

all_books = []

while True:
    try:
        logging.info(f"Запрос страницы: {url}")  # Используем URL напрямую

        response = session.get(url, headers=headers)
        response.raise_for_status()  # Проверка на ошибки HTTP (200 OK, и т.д.)
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('article', {'class': 'product_pod'})

        logging.info(f"Найдено {len(books)} книг на странице {url}")

        if not books:
            logging.info("Не найдено книг на текущей странице (вероятно, конец)")
            break

        for book in books:
            book_info = {}

            # Title
            try:
                book_info['title'] = book.find('h3').find('a').get('title')
            except AttributeError:
                book_info['title'] = None
                logging.warning("Не удалось извлечь название книги.")

            # URL
            book_info['url'] = None
            h3_element = book.find('h3')
            if h3_element:
                href = h3_element.get('href')
                if href:
                    book_info['url'] = urllib.parse.urljoin(base_url, href)  # Используем urljoin с базовым URL
            if book_info['url'] is None:
                logging.warning("Не удалось извлечь URL книги.")

            # Price
            try:
                price = book.find('div', {'class': 'product_price'}).getText()
                price = price.replace(',', '.')
                book_info['price'] = float(re.sub(r'[^\d.]+', '', price))
            except (AttributeError, ValueError):
                book_info['price'] = None
                logging.warning("Не удалось извлечь цену книги.")

            # Available (Availability)
            try:
                available_text = book.find('p', {'class': 'instock availability'}).getText(strip=True)
                book_info['available'] = int(re.sub(r'[^\d.]+', '', available_text))
            except (AttributeError, ValueError):
                book_info['available'] = None
                logging.warning("Не удалось извлечь количество доступных книг.")

            all_books.append(book_info)

        # Поиск кнопки "Next" и получение URL следующей страницы
        next_button = soup.find('li', {'class': 'next'})  # Поиск элемента "Next"
        if next_button:
            next_page_href = next_button.find('a').get('href')  # Извлекаем href
            url = urllib.parse.urljoin(base_url, next_page_href) # Формируем абсолютный URL для следующей страницы
        else:
            logging.info("Кнопка 'Next' не найдена - конец пагинации.")
            break  # Останавливаем цикл, если кнопки "Next" нет

    except requests.exceptions.HTTPError as e:
        logging.error(f"Ошибка HTTP при запросе страницы {url}: {e}")  # Используем текущий URL
        break  # Останавливаем цикл при ошибке HTTP
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка соединения: {e}")
        break
    except Exception as e:
        logging.error(f"Неожиданная ошибка при обработке страницы {url}: {e}") # Используем текущий URL
        break

df = pd.DataFrame(all_books)
print(df.info())
df.to_csv('books.csv', index=False)
logging.info("Данные сохранены в books.csv")


