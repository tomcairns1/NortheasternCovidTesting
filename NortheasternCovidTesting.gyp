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
import math

# The code to scrape data on this page was modeled after the code in the following article by Kerry Parker:
# https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f
urlpage = 'https://news.northeastern.edu/coronavirus/reopening/testing-dashboard/'
driver = webdriver.Firefox(executable_path='/Users/tomcairns/Desktop/Random Projects/JSScraper/geckodriver')
driver.get(urlpage) # Want to figure out how to hide this
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
df = pd.DataFrame(data, columns=['Date', 'Tests Completed', 'Negative Tests', 'Negative Rate', 'Positive Tests', 
'Positive Rate', 'MA Positive Rate'])
df['Date'] = pd.to_datetime(df['Date'])
df = df.reindex(index=df.index[::-1]) # Have to reverse DataFrame so it goes from oldest date to most recent
df.reset_index(inplace=True, drop=True)

# Find the susceptible population for each day
df['Total Population'] = 0

# This function finds the total population on campus for any given day, not number of susceptible individuals
def find_total_population():
    '''
    This function seeks to determine the number of total individuals on campus any particular day. This assumes that people
    are following the NU testing guidelines where initially one has to get tested on the 1st, 3rd, and 5th day of being on 
    campus and then every 3 days after that. This should give a rough estimate for the number of toal people. 
    '''
    i = 0
    while (i < len(df.index)):
        num_negative = int(df['Negative Tests'][i])
        if i == 0:
            df.loc[i, 'Total Population'] = num_negative
        elif i in [1, 2]:
            df.loc[i, 'Total Population'] = df.loc[(i - 1), 'Total Population'] + num_negative
        else:
            if num_negative < df.at[(i - 3), 'Total Population']:
                df.loc[i, 'Total Population'] = df.loc[(i - 1), 'Total Population']
            else:
                df.loc[i, 'Total Population'] = df.loc[(i - 1), 'Total Population'] + (num_negative - 
                df.loc[(i - 3), 'Total Population'])
        i += 1

# Find the rate of change for SIR model for each day
df['Susceptible Population'] = 0
df['Total Infected'] = 0
df['Change in Susceptible'] = 0
df['Actual Change in Susceptible'] = 0

def find_total_infected():
    '''
    This function is to find the total number of infected
    '''
    i = 0
    while (i < len(df.index)):
        if i == 0:
            df.loc[i, 'Total Infected'] = int(df.loc[i, 'Positive Tests'])
        else:
            df.loc[i, 'Total Infected'] = df.loc[i - 1, 'Total Infected'] + int(df.loc[i, 'Positive Tests'])

        i += 1

def find_susceptible_population():
    '''
    Find the actual number of susceptible people each day
    '''
    i = 0
    while (i < len(df.index)): 
        df.loc[i, 'Susceptible Population'] = df.loc[i, 'Total Population'] - df.loc[i, 'Total Infected']

        i += 1


def actual_change_in_susceptible():
    '''
    This function uses the S' function in the SIR model to find the rate of change in the susceptible population
    I might be able to compare it to the actual value to see how accurate it is / maybe adjust values of B
    '''
    i = 0
    while (i < len(df.index)):
        if i == 0:
            df.loc[i, 'Actual Change in Susceptible'] = 0
        elif df.loc[i, 'Total Population'] < max(df['Total Population']):
            df.loc[i, 'Actual Change in Susceptible'] = 0
            # Making it 0 for now since I don't know how to find rate of change when population is increasing
        else:
            # This will include first day of total population, but ignore that change for now
            df.loc[i, 'Actual Change in Susceptible'] = df.loc[i - 1, 'Susceptible Population'] - \
                df.loc[i, 'Susceptible Population']  

        i += 1



# I think a good idea would be to go through the more basic equations in the SIR model
# calculate the change in susceptible population, use that to figure out number of infected
# also can figure out the number of recovered. I really want to see if I can model the day-by-day change
# like can I make a model that can accurately predict the number of cases that will be found tomorrow? The next day?
# How many days in the future? And then based on that can I look at the long term projections to see how many
# people might be infected by the end of the semester? Could be helpful to figure out if the current strategies
# are effective or if they need to be changed. 

# Run the functions
find_total_population()
find_total_infected()
find_susceptible_population()
actual_change_in_susceptible()
# change_in_susceptible()
print(df)

# expected_infected() # All the issues, need to make sure equation is right and model is correct
# print(df)

# Create graph showing comparison of positive transmission rates between NU and MA
x_values = df['Date'].values # Want to remove the year from this
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


