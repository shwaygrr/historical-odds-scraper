
Scrapes historical basketball game odds data for a target season using Selenium and saves it as a CSV file.

#### Usage

1. Create a `.env` file and add the environement variables specificed in `.env.example` file.
```ini
# Path to ChromeDriver for Selenium automation
CHROME_DRIVER_PATH=C:/Users/your_username/chromedriver-win64/chromedriver.exe

# Path to store CSV files
CSV_PATH=C:/Users/your_username/Downloads/
```

2. Initialize scraper in `main.py` and pass in the target basketball season
```python
season = 2021 # target season 
scraper = Scraper(season)
data = scraper.ScrapeSeason()
scraper.SavetoCsv(data) # to save data as csv
```



