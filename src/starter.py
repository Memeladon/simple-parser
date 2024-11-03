from src.services import QuotesScraper
from src.services.site_manager import SiteManager


def main():
    """
            Основная функция запуска приложения.
    """
    # Регистрируем скрипт-скрапер для цитат
    manager = SiteManager()
    manager.register_scraper("quotes", QuotesScraper)

    url = "https://quotes.toscrape.com/"
    # url = "https://quotes.toscrape.com/page/7/"

    result = manager.scraping_site("quotes", url)
    if result:
        print(f"Успешно запарсил {len(result)} цитат.")
    else:
        print("Не удалось выполнить скрейпинг.")


if __name__ == "__main__":
    main()
