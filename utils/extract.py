import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}


def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.HTTPError:
        return None
    except requests.exceptions.Timeout:
        return None
    except Exception:
        return None


def scrape_page(soup, timestamp):
    products = []

    cards = soup.find_all("div", class_="collection-card")

    for card in cards:
        title = card.find("h3", class_="product-title")
        price = card.find("span", class_="price")
        product = {}
        product["Title"] = title.text.strip() if title else None
        product["Price"] = price.text.strip() if price else None
        paragraphs = card.find_all("p")
        for p in paragraphs:
            text = p.text.strip()
            if "Rating" in text:
                product["Rating"] = text
            elif "Colors" in text:
                product["Colors"] = text
            elif "Size" in text:
                product["Size"] = text
            elif "Gender" in text:
                product["Gender"] = text
        product["timestamp"] = timestamp

        products.append(product)

    return products


def scrape_all_pages():
    all_products = []

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for page in range(1, 51):
        if page == 1:
            url = "https://fashion-studio.dicoding.dev"
        else:
            url = f"https://fashion-studio.dicoding.dev/page{page}"

        soup = fetch_page(url)
        products = scrape_page(soup, timestamp)
        all_products.extend(products)
    return all_products


if __name__ == "__main__":
    products = scrape_all_pages()
    print(f"Total produk: {len(products)}")
    print(products)
