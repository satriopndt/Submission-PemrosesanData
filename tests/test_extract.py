import sys 
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from utils.extract import fetch_page, scrape_page, scrape_all_pages

def test_fetch_page_success():
    mock_response = MagicMock()
    mock_response.text = "<html><body><p>Test</p></body></html>"
    mock_response.raise_for_status = MagicMock()

    with patch("utils.extract.requests.get", return_value=mock_response):
        result = fetch_page("https://fashion-studio.decoding.dev")

    assert result is not None

def test_fetch_page_connection_error():
    import requests
    with patch("utils.extract.requests.get", side_effect=requests.exceptions.ConnectionError):
        result = fetch_page("https://fashion-studio.dicoding.dev")
    assert result is None

def test_scrape_page_normal():
    html = """
    <div class="collection-card>
        <h3 class="product-title">T-shirt 1</h3>
        <span class="price">$10.00</span>
        <p>Rating: ⭐ 4.5 / 5</p>
        <p>3 Colors</p>
        <p>Size: M</p>
        <p>Gender: Men</p>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = scrape_page(soup, "2025-01-01")
    assert result == []

def test_scrape_page_empty():
    soup = BeautifulSoup("<html></html>", "html.parser")
    result = scrape_page(soup, "2024-01-01")
    assert result == []

def test_scrape_page_timestamp():
    html = """
    <div class="collection-card">
        <h3 class="product-title">T-shirt 1</h3>
        <span class="price">$10.00</span>
        <p>Rating: ⭐ 4.5 / 5</p>
        <p>3 Colors</p>
        <p>Size: M</p>
        <p>Gender: Men</p>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    result = scrape_page(soup, "2024-01-01")
    assert result[0]["timestamp"] == "2024-01-01"

def test_scrape_all_pages():
    html = """
    <div class="collection-card">
        <h3 class="product-title">T-shirt 1</h3>
        <span class="price">$10.00</span>
        <p>Rating: ⭐ 4.5 / 5</p>
        <p>3 Colors</p>
        <p>Size: M</p>
        <p>Gender: Men</p>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    with patch("utils.extract.fetch_page", return_value=soup):
        result = scrape_all_pages()
    assert len(result) == 50