import requests
from typing import List, Dict
from bs4 import BeautifulSoup
from src.services.base_scraper import Scraper
from urllib.error import URLError, HTTPError
from requests.exceptions import RequestException


class QuotesScraper(Scraper):
    """
            Класс для скрейпинга сайта цитат и сохранения результатов в JSON-файл.

            Attributes:
                base_url (str): Базовый URL сайта цитат.
                all_quotes (List[Dict]): Список всех найденных цитат.
    """

    def __init__(self, base_url: str = "https://quotes.toscrape.com", max_pages: int = 100):
        self.base_url = base_url
        self.max_pages = max_pages
        self.quotes_on_the_page = 10  # Значение, отвечающее за количество цитат на странице
        self.all_quotes = []

    def scraping(self, url: str) -> List[Dict]:
        """
               Скрейпит страницу цитат и возвращает список словарей с информацией о цитатах.

               Args:
                   url (str): URL страницы для скрейпинга.

               Returns:
                   List[Dict]: Список словарей, где каждый словарь содержит информацию о цитате.

               Raises:
                   ValueError: Если возникли проблемы при скрейпинге или обработке данных.
        """
        try:
            page_content = self._make_request(url)
            soup = BeautifulSoup(page_content, 'html.parser')

            quotes = []
            quote_elements = soup.find_all('div', class_='quote')

            for element in quote_elements:
                text = element.find('span', class_='text').text.strip()
                author = element.find('small', class_='author').text.strip()

                tags = [tag.text.strip().lower() for tag in element.find_all('a', class_='tag')]
                quote = {
                    'text': text,
                    'author': author,
                    'tags': tags
                }
                quotes.append(quote)

            next_page_url = soup.find('li', class_='next')
            if next_page_url and next_page_url.a['href']:
                next_page_url = f"{self.base_url}{next_page_url.a['href']}"

                # Проверка на превышение максимального количества страниц в запросе
                if len(self.all_quotes) >= self.max_pages * self.quotes_on_the_page:
                    print(f"Максимальное количество страниц ({self.max_pages}) достигнуто.")
                    return self.all_quotes

                # Продолжаем скрейпинг следующих страниц
                all_quotes = self.scraping(next_page_url)
                return quotes + all_quotes
            else:
                return quotes

        except Exception as e:
            error_message = f"Ошибка при скрейпинге URL '{url}': {str(e)}"
            print(error_message)
            raise ValueError(error_message)

    def _make_request(self, url: str) -> str:
        """
               Выполняет HTTP-запрос к указанному URL и возвращает содержимое страницы.

               Args:
                   url (str): URL для выполнения запроса.

               Returns:
                   str: Содержимое страницы.

               Raises:
                   ValueError: Если возникли проблемы при выполнении запроса.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except HTTPError as e:
            raise ValueError(f"HTTP ошибка при запросе к URL: {e}")
        except URLError as e:
            raise ValueError(f"Невозможно подключиться к серверу: {e}")
        except RequestException as e:
            raise ValueError(f"Проблема с сетью при запросе к URL: {e}")

    def get_all_quotes(self) -> List[Dict]:
        """
                Получает все цитаты, если они еще не были загружены, и возвращает список словарей с информацией о цитатах.

                Returns:
                    List[Dict]: Список словарей, где каждый словарь содержит информацию о цитате.

                Note:
                    Если возникнут проблемы при загрузке цитат, метод вернет пустой список.
        """
        if not self.all_quotes:
            start_url = f"{self.base_url}/page/1"
            try:
                self.all_quotes = self.scraping(start_url)
            except ValueError as e:
                print(f"Не удалось загрузить цитаты: {e}")
                self.all_quotes = []  # Если произошла ошибка,то пустой массив
        return self.all_quotes

    def get_all_tags(self) -> List[str]:
        """
               Получает все уникальные теги из всех цитат и возвращает список строковых тегов.

               Returns:
                   List[str]: Список уникальных тегов.

               Note:
                   Если возникнут проблемы при получении тегов, метод вернет пустой список.
        """
        try:
            return list(set(tag.lower() for quote in self.all_quotes for tag in quote['tags']))
        except KeyError as e:
            error_message = f"Ошибка при получении тегов: {str(e)}."
            print(error_message)
            return []  # Если произошла ошибка,то пустой массив
