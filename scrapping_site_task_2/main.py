# main.py
import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "http://quotes.toscrape.com"

def get_soup(url): # функція для отримання і парсингу сторінки
    """Повертає об'єкт BeautifulSoup для заданої URL-адреси."""
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def parse_author(author_url): # функція для парсингу сторінки автора
    """Парсить сторінку автора і повертає словник з інформацією про нього."""
    soup = get_soup(author_url)
    fullname = soup.select_one("h3.author-title").get_text(strip=True)
    born_date = soup.select_one("span.author-born-date").get_text(strip=True)
    born_location = soup.select_one("span.author-born-location").get_text(strip=True)
    description = soup.select_one("div.author-description").get_text(strip=True)
    
    return {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }


def scrape_quotes_and_authors(base_url): 
    """Збирає всі цитати та авторів з сайту"""
    quotes_data = [] # збереження цитат
    authors_urls = {} # збереження унікальних URL авторів

    page_url = "/page/1/"
    while page_url:
        soup = get_soup(base_url + page_url) # отримання і парсинг сторінки
        quotes = soup.select("div.quote") # вибір всіх цитат на сторінці


# парсинг кожної цитати(забираємо дані, які знаходяться в середині div .quote)
        for el in quotes: 
            tags = [tag.get_text() for tag in el.select("div.tags a.tag")]
            author = el.select_one("small.author").get_text()
            quote = el.select_one("span.text").get_text()

            quotes_data.append({
                "tags": tags,
                "author": author,
                "quote": quote
            })

            # Зберігаємо посилання на автора, щоб потім спарсити
            link_author = el.select_one("span a")["href"]
            if author not in authors_urls: 
                authors_urls[author] = base_url + link_author 

        # Перехід до наступної сторінки(якщо кнопка є на сторінці ,переходимо на наступну сторінку інакше вихід з циклу)
        next_button = soup.select_one(".pager .next a")
        page_url = next_button["href"] if next_button else None

    # Парсинг інформації про авторів
    authors_list = []
    for url in authors_urls.values(): # Перебираємо всі унікальні посилання на авторів(значення словника-url)
        author_data = parse_author(url) # парсимо автора за його url і отрмання його даних у вигляді словника)
        authors_list.append(author_data) 

    # Зберігаємо в JSON
    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes_data, f, ensure_ascii=False, indent=2)

    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(authors_list, f, ensure_ascii=False, indent=2)

    print("Дані збережені в quotes.json та authors.json")


if __name__ == "__main__":
    scrape_quotes_and_authors(BASE_URL)