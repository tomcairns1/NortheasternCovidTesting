'''
Web Scraper to obtain and compare Northeastern's tesing and covid cases to MA average and what would be expected
without the implemented precautions

Steps:
- Create a graph of the number of positive tests compared to what would be expected
'''

import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver # this is to access the js created elements on the webpage
import time
import matplotlib.pyplot as plt 

# The code to scrape data on this page was modeled after the code in the following article by Kerry Parker:
# https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f
urlpage = 'https://news.northeastern.edu/coronavirus/reopening/testing-dashboard/'
driver = webdriver.Firefox(executable_path='/Users/tomcairns/Desktop/Random Projects/JSScraper/geckodriver')
driver.get(urlpage)
time.sleep(3)

# Obtain the data from the table
rows = driver.find_elements_by_xpath('//*[@id="dashboard-grid"]/div[5]/table/tbody/tr')
data = []
for row in rows:
    row_text = row.text.split() # Split all the data from the row
    data.append(row_text)

# Close driver
driver.quit()

# Save the data to a pandas df and convert date column to datetime
df = pd.DataFrame(data, columns=['Date', 'Tests Completed', 'Negative Tests', 'Negative Rate', 'Positive Tests', 'Positive Rate', 'MA Positive Rate'])
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')

# Create graph showing comparison of positive transmission rates between NU and MA
x_values = df.index.values # Want to remove the year from this
nu_transmission = [float(rate[:-1]) for rate in df['Positive Rate']] # convert string data to floats
ma_transmission = [float(rate[:-1]) for rate in df['MA Positive Rate']]

plt.plot(x_values, nu_transmission, color='red', label='NU Transmission Rate')
plt.plot(x_values, ma_transmission, color='blue', label='MA Transmission Rate')
plt.xlabel('Date')
plt.xticks(rotation=65)
plt.ylabel('Positive Transmission Rate')
plt.title('Positive Transmission Rate at Northeastern University compared to MA')
plt.legend(frameon=False)
plt.show()

# Create positive number of cases compared to what would be expected with MA transmission rates

