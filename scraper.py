"""
Web scraping module.
"""
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from urllib.parse import urljoin, urlparse
from webdriver_manager.chrome import ChromeDriverManager

from settings import BASE_URL, SKIP_EXTENSIONS, get_driver_options


class Scraper:
    """Web scraper class."""
    def __init__(self, links_to_scrape: list, visited_links: set):
        """Initializes the web scraper."""
        options = get_driver_options()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.links_to_scrape = links_to_scrape
        self.visited_links = visited_links
        self.cookies_accepted = False

    def __del__(self):
        """Destructor to close the WebDriver."""
        self.driver.quit()
    
    def scrape_next_page(self):
        """Scrapes a page and extracts content + links."""
        index = 0
        while index < len(self.links_to_scrape):
            url = self.links_to_scrape[index]

            if url in self.visited_links or not self.is_valid_page(url):
                index += 1
                continue  # Avoid duplicate visits or non-webpage URLs
        
            print(f"Scraping: {url}")
            self.driver.get(url)
            self._wait_for_page_load()

            # Handle cookie banner.
            if not self.cookies_accepted:
                self._accept_cookies()

            # Scrape the page content.
            content_divs = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='content_text']")
            page_text = "\n".join([div.text.strip() for div in content_divs if div.text.strip()])
            scraped_data = {url: page_text}

            # Extract all links.
            links = self.driver.find_elements(By.TAG_NAME, "a")
            all_links = self._extract_all_links(links)
            
            new_links = all_links.difference(self.links_to_scrape)
            self.links_to_scrape.extend(new_links)
            self.visited_links.add(url)
            index += 1

            yield scraped_data, list(new_links)

    def _accept_cookies(self):
        """Detects and clicks the 'Accept Cookies' button if present."""
        try:
            cookie_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'ldg-cookie__btn')]")
            cookie_button.click()
            self.cookies_accepted = True
            print("Accepted cookies.")
            self._wait_for_page_load()
        except Exception:
            # No cookie popup found.
            pass
    
    def _wait_for_page_load(self):
        """Waits for the entire page to load completely."""
        WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    
    def _extract_all_links(self, links):
        """Extracts all links from a list of web elements."""
        new_links = set()

        for link in links:
            try:
                href = link.get_attribute("href")
            except Exception:
                print("Skipping link with no href attribute.")
                continue
            if href:
                absolute_url = urljoin(BASE_URL, href)  # Convert relative URLs to absolute
                parsed_url = urlparse(absolute_url)

                # Only follow links within the same domain
                if parsed_url.netloc == urlparse(BASE_URL).netloc and self.is_valid_page(absolute_url):
                    new_links.add(absolute_url)
        
        return new_links


    @staticmethod
    def is_valid_page(url):
        """Check if a URL is a valid webpage and not a file."""
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()
        
        # Skip URLs that end with unwanted file extensions
        return not any(path.endswith(ext) for ext in SKIP_EXTENSIONS)
