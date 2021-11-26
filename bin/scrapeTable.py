#!/usr/bin/env python3
'''
Filename: scrapeTable.py

This file scrapes a jaascript table from the Northeastern Covid Testing
Dashboard: https://news.northeastern.edu/coronavirus/reopening/testing-dashboard/.

How to run:
python3 scrapeTable.py
'''

import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

# Let us Begin
url = 'https://news.northeastern.edu/coronavirus/reopening/testing-dashboard/'

# Run the webdriver
driver = webdriver.Firefox(executable_path='/Users/tomcairns/Downloads') 
# I'm having issues finding the correct executable path for my geckodriver

driver.get(url)
