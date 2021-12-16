'''
Filename: 
NortheasternCovidTesting.py

Purpose:
Web Scraper to obtain and analyze Northeastern's covid testing strategy

How to Execute:
$ python3 NortheasternCovidTesting.py --o output.csv
'''

##################
# Import Libraries
##################

import argparse
import math
import time
import urllib.request
import matplotlib.pyplot as plt 
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


def main():
    '''Business Logic'''
    # Read in the command line arguments
    args = get_cli()
    print(f"Command Arguments are: {args}")

    # Code adapted from (Parker, 2020)
    urlpage = 'https://news.northeastern.edu/coronavirus/reopening/testing-dashboard/'
    driver = webdriver.Firefox()
    driver.get(urlpage) # Want to figure out how to hide this
    time.sleep(1)

    # Obtain the data from the table
    data = findRows(driver)
    print(f"First data: {data}")
    # This did not properly scrape

    # Close the driver
    driver.quit()

    # Change data into a dataframe
    df = convertToDataframe(data)
    print(f"When Converted to df: {df}")

    # Find the rate of change
    df = findRateOfChange(df)
    print(f"Incuding the rate of Change: {df}")

    # Save to File
    df.to_csv(args.output)
    print('success')



def findRows(driver):
    '''
    Function: findRows
    Parameters: driver (webdriver)
    Outputs: Data (list)
    Purpose: This function finds the rows in the website and saves to a dataframe
    '''
    _clickButton(driver)
    rows = driver.find_elements_by_xpath('//*[@id="data-table"]/div/table/tbody')

    # Save to a dataframe
    for row in rows:
        print(f'row = {row}')
        row_text = row.text.split()
        print(f'Row text is {row_text}')

    return row_text


def _clickButton(driver):
    ''' 
    Function: _clickButton
    Paramters: driver (webdriver)
    Outputs: None
    Purpose: This function clicks the "Show More" button to get the whole table
    Code adapted from [2]
    '''
    cookie_button = driver.find_elements_by_xpath('/html/body/div[4]/button')[0]
    print(f'Cookie button: {cookie_button}')
    cookie_button.click()

    # Sleep for a second
    time.sleep(3)

    # Get the location of the button
    load_more_btn = driver.find_elements_by_xpath('/html/body/div[1]/main/article/div[3]/div/div[2]/div/section[6]/button')[0]

    # Click the button
    load_more_btn.click()


def convertToDataframe(dataset):
    '''
    Function: convertToDataFrame
    Parameters: dataset (list)
    Outputs: df (dataframe)
    Purpose: This function converts the row data to a dataframe
    '''
    # Convert to a list of lists
    dataset_lol = _buildListofLists(dataset)

    # Convert to data frame
    df = pd.DataFrame(dataset_lol, columns=['Date', 'Tests Completed', 'Negative Tests', 
                                     'Negative Rate', 'Positive Tests', 
                                     'Positive Rate'])

    # Convert date to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Reverse the data frame to start with oldest date
    df = df.reindex(index=df.index[::-1])
    df.reset_index(inplace=True, drop=True)

    return df


def _buildListofLists(dataset):
    ''' 
    Function: _buildListofLists
    Parameters: dataset (list)
    Outputs: dataset_lol (list of lists)
    Purpose: This function converts the list into a list of lists to later be
    converted into a dataframe
    '''
    # Convert to list of lists
    dataset_lol = [dataset[x : x+6] for x in range(0, len(dataset), 6)]

    return dataset_lol


def findRateOfChange(dataframe):
    ''' 
    Function: findRateOfChange
    Parameters: dataframe
    Output: dataframe
    Purpose: This function finds the rate of change in the positive transmission rate
    '''
    dataframe['NU RoC'] = 0
    # df['MA RoC'] = 0

    # Calculate the rate of change
    for row in dataframe.index:
        if row != 0:
            dataframe.loc[row, 'NU RoC'] = float(dataframe.loc[row, 'Positive Rate'][:-1]) - float(dataframe.loc[row - 1, 'Positive Rate'][:-1])

    return dataframe


def get_cli():
    ''' 
    Parameters: None
    Output: cli (command line instance)
    Purpose: This function gets the command line arguments
    '''
    parser = argparse.ArgumentParser(description = 'Give Output File')

    # Add arguments
    parser.add_argument('-output', '--o', dest = 'output', type = str,
                        help = 'Name of Output File', required = False,
                        default = '../data/output.csv')

    return parser.parse_args()


############################################################
# Scrape data from news.northeastern covid testing dashboard
############################################################

# Obtain the data from the table
# rows = driver.find_elements_by_xpath('//*[@id="dashboard-grid"]/div[5]/table/tbody/tr')
# data = []
# for row in rows:
#     row_text = row.text.split() # Split all the data from the row
#     data.append(row_text)

# # Close driver
# driver.quit()

# # Save the data to a pandas df and convert date column to datetime
# df = pd.DataFrame(data, columns=['Date', 'Tests Completed', 'Negative Tests', 
# 'Negative Rate', 'Positive Tests', 'Positive Rate'])
# df['Date'] = pd.to_datetime(df['Date'])
# df = df.reindex(index=df.index[::-1]) # Have to reverse DataFrame so it goes from oldest date to most recent
# df.reset_index(inplace=True, drop=True)

# Add in the columns for change in transmission rate for MA and NU
# df['NU RoC'] = 0
# df['MA RoC'] = 0

# for row in df.index:
#     if row != 0:
#         df.loc[row, 'NU RoC'] = float(df.loc[row, 'Positive Rate'][:-1]) - float(df.loc[row - 1, 'Positive Rate'][:-1])
        # df.loc[row, 'MA RoC'] = float(df.loc[row, 'MA Positive Rate'][:-1]) - float(df.loc[row - 1, 'MA Positive Rate'][:-1])
        

if __name__ == '__main__':
    main()




##########
# Sources
##########

'''
[1] Parker, K. (2020, June 25). Data Science Skills: Web scraping javascript using 
python. Retrieved September 27, 2020, from 
https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f

[2] https://stackoverflow.com/questions/37341667/click-on-show-more-button-on-nytimes-com-with-selenium
'''

