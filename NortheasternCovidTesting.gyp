'''
Web Scraper to obtain and analyze Northeastern's covid testing strategy
'''

##################
# Import Libraries
##################

import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
import time
import matplotlib.pyplot as plt 
import math


############################################################
# Scrape data from news.northeastern covid testing dashboard
############################################################

# Code adapted from (Parker, 2020)
urlpage = 'https://news.northeastern.edu/coronavirus/reopening/testing-dashboard/'
driver = webdriver.Firefox(executable_path='/Users/tomcairns/Desktop/Random Projects/JSScraper/geckodriver')
driver.get(urlpage) # Want to figure out how to hide this
time.sleep(2)

# Obtain the data from the table
rows = driver.find_elements_by_xpath('//*[@id="dashboard-grid"]/div[5]/table/tbody/tr')
data = []
for row in rows:
    row_text = row.text.split() # Split all the data from the row
    data.append(row_text)

# Close driver
driver.quit()

# Save the data to a pandas df and convert date column to datetime
df = pd.DataFrame(data, columns=['Date', 'Tests Completed', 'Negative Tests', 'Negative Rate', 'Positive Tests', 
'Positive Rate', 'MA Positive Rate'])
df['Date'] = pd.to_datetime(df['Date'])
df = df.reindex(index=df.index[::-1]) # Have to reverse DataFrame so it goes from oldest date to most recent
df.reset_index(inplace=True, drop=True)

###################
# Visualize Results
###################

# Create graph showing comparison of positive transmission rates between NU and MA
x_values = df['Date'].values # Want to remove the year from this
nu_transmission = [float(rate[:-1]) for rate in df['Positive Rate']] # convert string data to floats
ma_transmission = [float(rate[:-1]) for rate in df['MA Positive Rate']]

plt.plot(x_values, nu_transmission, color='red', label='NU Transmission Rate')
plt.plot(x_values, ma_transmission, color='blue', label='MA Transmission Rate')
plt.xlabel('Date')
plt.xticks(rotation=65)
plt.ylabel('% Positive Transmission Rate')
plt.title('Positive Transmission Rate at Northeastern University compared to MA')
plt.legend(frameon=False)
plt.show()


#########
# Sources
#########

# Parker, K. (2020, June 25). Data Science Skills: Web scraping javascript using python. Retrieved September 27, 2020, 
# from https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f