# Using Google Colab and Google-Colab-Selenium to obtain data from: https://nuforc.org/subndx/?id=cUnited_Kingdom 

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %pip install -q google-colab-selenium

import google_colab_selenium as gs
import pandas as pd

from selenium.webdriver.common.by import By

import time

driver = gs.Chrome()

# test connection and quit driver
driver.get('https://nuforc.org/subndx/?id=cUnited_Kingdom')
print(driver.title)
driver.quit()

# Code below taken and edited from https://github.com/jpjacobpadilla/Google-Colab-Selenium

from selenium.webdriver.chrome.options import Options

# Instantiate options
options = Options()

# Add extra options
options.add_argument("--disable-infobars")  # Disable the infobars
options.add_argument("--disable-popup-blocking")  # Disable pop-ups
options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors
options.add_argument("--incognito")  # Use Chrome in incognito mode

driver = gs.Chrome(options=options)

driver.get('https://nuforc.org/subndx/?id=cUnited_Kingdom')
print(driver.title)

# Creating Function to Scrape Data from Dynamic Table: 

date_and_time_reported = []
cities = []
summaries = []

def scrape_website():
    
    # Find the data

    reported_date = driver.find_elements(By.XPATH, '//td[@class="column-occurred sorting_1"]')
    city = driver.find_elements(By.XPATH, '//td[@class="   column-city"]')
    summary = driver.find_elements(By.XPATH, '//td[@class="   column-summary"]')

    print(f'There are {len(reported_date), len(city), len(summary)}  for dates, cities and summaries on this page')

    # Extract each data point and add them to the relevant list

    for date in range(len(reported_date)):
      date_and_time_reported.append(reported_date[date].text)

    for each_city in range(len(city)):
      cities.append(city[each_city].text)

    for each_summary in range(len(summary)):
      summaries.append(summary[each_summary].text)

# Scrape first table page

scrape_website()

# Start scraping loop from 2nd page by first clicking the next page button

start_time = time.time()

for page in range(2, 40):


  nextpage = driver.find_element(By.CLASS_NAME, 'paginate_button.next')
  nextpage.click()

  time.sleep(5)

  print(f'Scraping Page Number: {page}')
  scrape_website()

end_time = time.time()

print(f'This took {start_time - end_time} seconds to run')

# Create DataFrame and Convert to Excel

df_all_ufo_data = pd.DataFrame({'Date and Time Reported': date_and_time_reported, 'City': cities, 'Summary': summaries})

ufo_data_csv = df_all_ufo_data.to_csv('ufo_data.csv', index=False)