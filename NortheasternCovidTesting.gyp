'''
Web Scraper to obtain and analyze Northeastern's covid testing strategy
'''

##############
# Import Libraries
##############

import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
import time
import matplotlib.pyplot as plt 
import math


##############
# Scrape data from news.northeastern covid testing dashboard
##############

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


##############
# Calculate Susceptible, Infected, and Recovered Populations
##############

# Initialize New Columns in df
df['Total Population'] = 0
df['Susceptible Population'] = 0
df['Total Infected'] = 0
df['Change in Susceptible'] = 0
df['Actual Change in Susceptible'] = 0
df['Number of Recovered'] = 0


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
    Find the actual number of susceptible people each day, making assumption that recovered people are immune
    '''
    i = 0
    while (i < len(df.index)): 
        df.loc[i, 'Susceptible Population'] = df.loc[i, 'Total Population'] - df.loc[i, 'Total Infected']

        i += 1


def actual_change_in_susceptible():
    '''
    Find the actual rate of change in the susceptible population
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
            df.loc[i, 'Actual Change in Susceptible'] = df.loc[i, 'Susceptible Population'] - \
                df.loc[i - 1, 'Susceptible Population']

        i += 1


def number_of_infected():
    '''
    Find the number of actively infected people, assuming 14 day recovery
    '''
    # I might have to first find the rate of change of Infected and then multiply that number by the number of infected? 
    # Need more thinking
    variable = 5
    print(type(variable))


def change_in_susceptible():
    '''
    Using the S' function in the SIR model to find the rate of change inthe susceptible population
    '''
    if i == 0:
        df.loc[i, 'Change in Susceptible'] = 0
    elif df.loc[i, 'Total Population'] < max(df['Total Population']):
        df.loc[i, 'Change in Susceptible'] = 0 # Not sure how I would change this
    else:
        # This will include first day of total population, ignore that rate of change for now
        positive_rate = df.loc[i, 'Positive Rate']
        susceptible_population = df.loc[i, 'Susceptible Population']
        # Need to find number of infected before implementing this


# Run the functions
find_total_population()
find_total_infected()
find_susceptible_population()
actual_change_in_susceptible()
# number_of_infected()
# change_in_susceptible()
print(df)


##############
# Create Graphs
##############

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


##############
# Sources
##############

# Parker, K. (2020, June 25). Data Science Skills: Web scraping javascript using python. Retrieved September 27, 2020, 
# from https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f