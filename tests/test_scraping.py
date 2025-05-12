# tests/test_scraping.py
import pytest
import os
from src.scraping import load_html_file, scrape_amazon_reviews, load_config

@pytest.fixture
def html_file_path():
    return os.path.join("data", "input", "fichier.html")

def test_load_html_file(html_file_path):
    content = load_html_file(html_file_path)
    assert isinstance(content, str)
    assert len(content) > 0

def test_load_config():
    config = load_config("config/config.json")
    assert isinstance(config, dict)
    assert all(key in config for key in ["name", "title", "comment"])
    assert any(key in config for key in ["rating", "date", "verified"])  # Optional keys

def test_scrape_amazon_reviews(html_file_path):
    reviews = scrape_amazon_reviews(html_file_path)
    assert isinstance(reviews, list)
    if reviews:
        assert all(isinstance(review, dict) for review in reviews)
        assert all(key in review for key in ["name", "title", "comment"] for review in reviews)
        assert all(key in review for key in ["rating", "date", "verified"] for review in reviews)