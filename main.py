"""
Main module.
"""
import orjson

from helpers import load_jsonl
from settings import BASE_URL
from scraper import Scraper


LINKS_TO_SCRAPE_FILE = "data/links_to_scrape.jsonl"
SCRAPED_DATA_FILE = "data/scraped_data.jsonl"


def main():
    """
    The main entry point of the application.
    """
    # Load visited links from JSON file.
    scraped_data = load_jsonl(SCRAPED_DATA_FILE, {})        
    visited_links = set(scraped_data.keys())

    # Load links to scrape from JSON file.
    links_to_scrape = load_jsonl(LINKS_TO_SCRAPE_FILE, [BASE_URL])

    # Initialize the Selenium WebDriver.
    scraper = Scraper(links_to_scrape, visited_links)

    # Save data to JSON files after each page scrape.
    with (
        open(SCRAPED_DATA_FILE, "ab") as scraped_data_file,
        open(LINKS_TO_SCRAPE_FILE, "wb") as links_to_scrape_file
    ):
        links_to_scrape_file.write(orjson.dumps(links_to_scrape) + b"\n")
        for new_data, new_links in scraper.scrape_next_page():
            scraped_data_file.write(orjson.dumps(new_data) + b"\n")
            if new_links:
                links_to_scrape_file.write(orjson.dumps(new_links) + b"\n")


if __name__ == "__main__":
    main()
