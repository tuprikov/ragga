"""
Settings for the web scraping project.
"""
from selenium import webdriver


BASE_URL = "https://www.leudelange.lu/fr/commune-de-leudelange/informations-pratiques"
CHROME_OPTIONS = [
    "--headless",
    "--disable-gpu",
    "--no-sandbox",
    "--enable-unsafe-swiftshader",
]
# List of file extensions to skip
SKIP_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".zip", ".mp4", ".mp3", ".docx", ".xlsx"}


def get_driver_options():
    """Returns the Chrome WebDriver options."""
    options = webdriver.ChromeOptions()
    for option in CHROME_OPTIONS:
        options.add_argument(option)
    return options
