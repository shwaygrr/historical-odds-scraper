from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import re
from game import Game

time_regex = r"^(?:[01]\d|2[0-3]):[0-5]\d$"

class SeasonScraper:
	def __init__(self, driver, start_year):
		self.driver = driver
		self.start_year = start_year
		self.end_year = start_year+1

	def __del__(self):
		self.driver.quit()

	def findNextButton(self):
		pagination = self.driver.find_elements(By.CLASS_NAME, "pagination-link")
		for page_link in pagination:
			if page_link.text == "Next":
				return page_link
		return None

	def scrapeSeason(self):
		end_year = self.start_year+1
		base_url = f"https://www.oddsportal.com/basketball/usa/nba-{self.start_year}-{self.end_year}/results/"
		self.driver.get(base_url)

		time.sleep(5)

		all_games = []

		while True:
			event_rows = self.driver.find_elements(By.CLASS_NAME, "eventRow")
			
			for event_row in event_rows:
				date = event_row.find_elements(By.CLASS_NAME, "leading-5")[0].text # dates
				all_games.append(date)


			# game_row = 

			# for game in game_rows:
			#     try:
			#         date =   
			#         teams = game.find_elements(By.CLASS_NAME, "leading-5")[0].text
			#         score = game.find_element(By.CLASS_NAME, "score").text
			#         all_games.append([year, teams, score])
			#     except Exception:
			#         continue
		# Skip if data is missing

			# Find next page button and click it
			next_button = self.findNextButton()
			if next_button is None:
				print(f"Finished scraping for {self.start_year}/{end_year}.")
				break
			else:
				ActionChains(self.driver).move_to_element(next_button).click().perform()
				time.sleep(3)

		return all_games

# Scrape data from 2020 to 2024

# all_data.extend(scrapeSeason(year))
# Save to CSV
# df = pd.DataFrame(all_data, columns=["Year", "Teams", "Score"])
# print(df)
# df.to_csv("nba_oddsportal_data.csv", index=False)
# print("Data successfully saved as nba_oddsportal_data.csv!")

'''
1. go to page
2. scrape table
   a. get date
   b. get games and data for games
   c. goto a if next games exist
3. click next
4. goto 1 if next exists 
'''
