import re
from datetime import date
import os
from abc import ABC, abstractmethod
import json
from typing import List, Dict


class Scraper(ABC):
    """
            Абстрактный класс для реализации скриптов-скреперов.

            Этот класс предоставляет базовую структуру для создания скриптов,
            которые могут скрейпить данные из веб-сайтов и сохранять их в JSON-файлы.
    """
    @abstractmethod
    def scraping(self, url: str) -> List[Dict]:
        """
                Абстрактный метод для выполнения скрейпинга указанной страницы.

                Args:
                    url (str): URL страницы для скрейпинга.

                Returns:
                    List[Dict]: Список словарей, где каждый словарь содержит информацию о скрейпеданных данных.

                Note:
                    Этот метод должен быть реализован в подклассах Scraper.
        """
        pass

    @classmethod
    def save_to_json(cls, data: List[Dict], url):
        """
                Сохраняет данные в JSON-файл с уникальным именем, основанным на имени сайта и дате.

                Args:
                    data (List[Dict]): Список словарей с данными для сохранения.
                    url (str): URL страницы, откуда были скрейпеданы данные.

                Note:
                    Если список данных пустой или не содержит URL, будет использовано значение 'unknown' для имени сайта.
        """
        current_date = date.today().strftime("%d_%m_%Y")
        site_name = cls._extract_site_name(url) if data else 'unknown'
        filename = f"data/{site_name}-{current_date}.json"
        cls._ensure_directory_exists(os.path.dirname(filename))
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _extract_site_name(url: str) -> str:
        """
                Извлекает имя сайта из URL.

                Args:
                    url (str): URL для анализа.

                Returns:
                    str: Имя сайта или 'unknown', если извлечение не удалось.

                Note:
                    Используется регулярное выражение для поиска имени хоста в URL.
        """
        match = re.search(r'https?://([^/]+)', url)
        return match.group(1) if match else 'unknown'

    @staticmethod
    def _ensure_directory_exists(directory: str):
        """
                Убеждается, что указанная директория существует, и создает ее, если она отсутствует.

                Args:
                    directory (str): Путь к директории для проверки.
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
