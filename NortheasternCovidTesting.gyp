'''
Web Scraper to obtain and keep track of Northeastern's tesing and covid cases

Steps:
- Create a web scraper to scrape data from the northeastern testing dashboard
- Create a graph of the number of positive tests compared to what would be expected
'''

import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver # this is to access the js created elements on the webpage
import time

# The code to access the data on this page was modeled after the code in the following article by Kerry Parker:
# https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f
urlpage = 'https://news.northeastern.edu/coronavirus/reopening/testing-dashboard/'
driver = webdriver.Firefox(executable_path='/Users/tomcairns/Desktop/Random Projects/JSScraper/geckodriver')
driver.get(urlpage)
time.sleep(10)

# Obtain the data from the table
rows = driver.find_elements_by_xpath('//*[@id="dashboard-grid"]/div[5]/table/tbody/tr')
data = []
for row in rows:
    row_text = row.text.split() # Split all the data from the row
    data.append(row_text)

# Close driver
driver.quit()

# Save the data to a pandas df
df = pd.DataFrame(data, columns=['Date', 'Tests Completed', 'Negative Tests', 'Negative Rate', 'Positive Tests', 'Positive Rate', 'MA Positive Rate'])
print(df)
