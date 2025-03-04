from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from scraper import SeasonScraper
import time
time_regex = r"^(?:[01]\d|2[0-3]):[0-5]\d$"

service = Service("C:/Users/15616/chromedriver-win64/chromedriver.exe")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

if __name__ == "__main__":
  scraper = SeasonScraper(driver, 2023)
  games = scraper.scrapeSeason()
  
  for index, game in enumerate(games):
    print(f"{index+1}. {game}")
  # print(len(games))