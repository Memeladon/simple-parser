class SiteManager:
    """
           Класс управляет процессом скрейпинга различных веб-сайтов.

           Этот класс предоставляет механизм регистрации скриптов-скраперов,
           управления ими и координации процесса скрейпинга.
    """
    def __init__(self):
        # Пустой словарь для хранения скриптов-скраперов.
        self.scrapers = {}

    def register_scraper(self, site_name: str, scraper_class):
        """
                Регистрирует новый скрипт-скрапер в менеджере.

                Args:
                    site_name (str): Уникальное имя сайта для регистрации.
                    scraper_class (class): Класс скрипта-скрапера для регистрации.
        """
        if site_name in self.scrapers:
            raise ValueError(f"Скрапер для сайта '{site_name}' уже зарегистрирован.")
        self.scrapers[site_name] = scraper_class()

    def unregister_scraper(self, site_name: str):
        """
        Отменяет регистрацию скрапера для указанного сайта.

        Args:
            site_name (str): Имя сайта, для которого нужно отменить регистрацию скрапера.

        Raises:
            ValueError: Если скрапер для указанного сайта не был зарегистрирован.

        Returns:
            None
        """
        if site_name not in self.scrapers:
            raise ValueError(f"Скрапер для сайта '{site_name}' не зарегистрирован.")
        del self.scrapers[site_name]

    def get_scraper(self, site_name: str):
        """
                Получает скрипт-скрапер по имени сайта.

                Args:
                    site_name (str): Имя сайта для получения соответствующего скрипта.

                Returns:
                    Scraper: Объект класса-скрапера, если он зарегистрирован, иначе None.
        """
        return self.scrapers.get(site_name)

    def scraping_site(self, site_name: str, url: str):
        """
                Выполняет процесс скрейпинга указанного сайта.

                Args:
                    site_name (str): Имя сайта для скрейпинга.
                    url (str): URL страницы для скрейпинга.

                Returns:
                    List[Dict]: Список словарей с данными, полученными от скрейпинга, или None, если скрейпинг не удался.

                Note:
                    Этот метод использует зарегистрированный скрипт-скрапер для сайта,
                    выполняет его на указанной URL и сохраняет результаты в JSON-файл.
        """
        scraper = self.get_scraper(site_name)
        if scraper:
            data = scraper.scraping(url)
            scraper.save_to_json(data, url)
            return data
        return None


