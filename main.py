from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from scraper import SeasonScraper
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

service = Service(Path(os.getenv("CHROME_DRIVER_PATH")))
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

if __name__ == "__main__":
    season = 2023
    scraper = SeasonScraper(driver, season)
    games = scraper.scrapeSeason()
    scraper.saveToCsv(games)
    scraper.quit()