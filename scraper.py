from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import re
from game import Game
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

class SeasonScraper:
	def __init__(self, driver, start_year):
		self.driver = driver
		self.start_year = start_year
		self.end_year = start_year+1
		self.date_regex = r"^\d{2} [A-Za-z]{3} \d{4}$"

	def rejectCookies(self):
		try:
			reject_button = WebDriverWait(self.driver, 8).until(
				EC.presence_of_element_located((By.ID, "onetrust-reject-all-handler"))
			)
			ActionChains(self.driver).move_to_element(reject_button).click().perform()
		except:
				pass

	def findNextButton(self):
		pagination = self.driver.find_elements(By.CLASS_NAME, "pagination-link")
		for page_link in pagination:
			if page_link.text == "Next":
				return page_link
		return None
	
	def getDate(self, event_row):
		poss_dates = event_row.find_elements(By.CLASS_NAME, "leading-5")
		for poss_date in poss_dates:
			text = poss_date.text
			if re.match(self.date_regex, text[0:11]):
				return text
		# print(f"Error retreiving date for list {[date.text for date in poss_dates]}")
		return None

	def getGameData(self, event_row, date):
		game_row = event_row.find_elements(By.CSS_SELECTOR, ".hover\\:bg-\\[\\#f9e9cc\\]")

		if len(game_row) != 1:
			print(f"Error with extracting game row in date: {date}")
			return None
		
		game_row = game_row[0]

		if game_row.find_elements("xpath", ".//*[contains(@class, 'text-red-dark')]"):
			return None

		team_els = game_row.find_elements(By.CLASS_NAME, "participant-name")
		odds = [int(num.text) for num in game_row.find_elements(By.CSS_SELECTOR, ".hover\\:\\!bg-gray-medium")]
		scores = [int(num.text) for num in game_row.find_elements(By.CSS_SELECTOR, "div.min-mt\\:\\!flex.hidden")]

		if len(team_els) != 2 or len(odds) != 2 or len(scores) != 2:
			print(date)
			print(team_els)
			print(odds)
			print(scores)
			print("Error: Game item length is not 2")
			self.__del__

		game_data = Game(
			date=date,
			time=game_row.find_elements(By.XPATH, "//p[@data-v-931a4162]")[0].text,
			home_team=team_els[0].text,
			away_team=team_els[1].text,
			pos_odds=max(odds) if len(odds) == 2 else "-",
			neg_odds=min(odds) if len(odds) == 2 else "-",
			home_points=scores[0],
			away_points=scores[1],
			winner=team_els[(scores.index(max(scores)))].text
		)
		return game_data
	
	def scrapeSeason(self):
		base_url = f"https://www.oddsportal.com/basketball/usa/nba-{self.start_year}-{self.end_year}/results/"
		self.driver.get(base_url)
		
		self.rejectCookies()

		all_games = []

		while True: # scrape entire season
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(2)

			event_rows = WebDriverWait(self.driver, 10).until(
				EC.presence_of_all_elements_located((By.CLASS_NAME, "eventRow"))
			)
			current_date = None
			for event_row in event_rows:
				date = self.getDate(event_row)
				
				if date is not None:
					current_date = date

				game = self.getGameData(event_row, current_date)
				if game is not None:
					all_games.append(game)	
			
			next_button = self.findNextButton()
			if next_button is None:
				print(f"Finished scraping for {self.start_year}/{self.end_year}.")
				break
			else:
				ActionChains(self.driver).move_to_element(next_button).click().perform()
		return all_games
	
	def saveToCsv(self, games, filename=None):
		if not filename:
			filename = f"{Path(os.getenv("CSV_PATH"))}/{self.start_year}_{self.end_year}.csv"
		
		# Convert list of Game objects to list of dictionaries
		game_dicts = [game.__dict__ for game in games]
		
		# Create DataFrame and save to CSV
		df = pd.DataFrame(game_dicts)
		df.to_csv(filename, index=False)
		print(f"Data saved to {filename}")
		return df











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
			# next_button = self.findNextButton()
			# if next_button is None:
			# 	print(f"Finished scraping for {self.start_year}/{end_year}.")
			# 	break
			# else:
			# 	ActionChains(self.driver).move_to_element(next_button).click().perform()
			# 	time.sleep(3)


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









	# def scrapeSeasonTest(self):
	# 	base_url = f"https://www.oddsportal.com/basketball/usa/nba-{self.start_year}-{self.end_year}/results/"
	# 	self.driver.get(base_url)

	# 	self.rejectCookies()

	# 	self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	# 	time.sleep(2)

	# 	event_rows = WebDriverWait(self.driver, 10).until(
  #   	EC.visibility_of_all_elements_located((By.CLASS_NAME, "eventRow"))
	# 	)
		
	# 	# print(len(event_rows))

	# 	all_games = []

	# 	for event_row in event_rows:
	# 		date = self.getDate(event_row)
	# 		if date is not None:
	# 			all_games.append(date)
	# 	return all_games
