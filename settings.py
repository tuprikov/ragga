"""
Settings for the web scraping project.
"""
import os

from selenium import webdriver


BASE_URL = "https://www.leudelange.lu/"
CHROME_OPTIONS = [
    "--headless",
    "--disable-gpu",
    "--no-sandbox",
    "--enable-unsafe-swiftshader",
]
ELASTIC_API_KEY = os.getenv('ELASTIC_API_KEY')  # Set your Elastic Cloud API key
ELASTIC_HOST = 'https://my-elasticsearch-project-ac5d2c.es.eu-west-1.aws.elastic.cloud:443'
LINKS_TO_SCRAPE_FILE = "data/links_to_scrape.jsonl"
SCRAPED_DATA_FILE = "data/scraped_data.jsonl"
SKIP_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".zip", ".mp4", ".mp3", ".docx", ".xlsx"}


mapping = {
    "settings": {
        "index": {
            "knn": True  # Enable approximate nearest neighbor (ANN) search
        }
    },
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "embedding": {
                "type": "dense_vector",
                "dims": None  # Will be set dynamically
            }
        }
    }
}


def get_driver_options():
    """Returns the Chrome WebDriver options."""
    options = webdriver.ChromeOptions()
    for option in CHROME_OPTIONS:
        options.add_argument(option)
    return options
