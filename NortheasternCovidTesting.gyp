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

# Have to do extra stuff since the webpage is built with js
# Check the article https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f for useful information
urlpage = 'https://news.northeastern.edu/coronavirus/reopening/testing-dashboard/'
print(urlpage)
driver = webdriver.Firefox(executable_path='/Users/tomcairns/Desktop/Random Projects/JSScraper/geckodriver')
driver.get(urlpage)
time.sleep(10)

# Obtain the data from the table
results = driver.find_elements_by_xpath('//*[@id="dashboard-grid"]/div[5]/table/tbody/tr')
print(len(results))

driver.quit()



