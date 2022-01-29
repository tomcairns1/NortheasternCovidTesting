# Northeastern Covid Testing Project

## Preface
I am not a healthcare professional or epidemiologist. This is a personal project 
as something to do just for fun. My analysis is my own and in no way should be 
taken as guidance in this pandemic.


## Introduction
This project is used to monitor the COVID-19 situation at Northeastern
University in Boston, MA. I believe the way the university displays and publishes
their data is not an effective representation. Therefore I have created this
project to visualize the data myself.

The goal of this program is to visually represent the trends in positive 
transmission rates and the change in rates between Massachusetts and Northeastern.


## Methods
The data used in this project was taken from the Northeastern Covid Testing 
dashboard found at the following URL: 
https://news.northeastern.edu/coronavirus/reopening/testing-dashboard/. 
Permission was given by news.northeastern to use this data.

*/bin*
The file `NortheasternCovidWebScraper.py` scrapes the data from this website using 
webdriver[1]. The code for this section was adapted from Parker 2020. The data 
was saved to a .csv file called `CopiedData.csv`.

The file `createDatabase.sql` contains the SQLite commands to create the database,
`NUCovid.db` to store all of the scraped data.

The file `createDatabase.py` is used to take the data from `CopiedData.csv` to
add to the database file, `NUCovid.db`.

The file `createDatabase.sh` is used to run both database creation files
(`createDatabase.sql` and `createDatabase.py`).

The file `analysis.R` is used to run the analysis of the data and save the
associated files into the ../figures directory.

The file `analysis.Rmd` is more exploratory in nature and is used to test the
code used to create the figures.

The file `pipeline.sh` is used to run the whole pipeline. It scrapes the data
from the Northeastern website, adds the data to the database, and then analyzes
the data and saves / updates the figures.

The file `obtainMAData.py` is a file to scrape the data from the Massachusetts
government and to take the Excel sheet from the file that contains the information
to then be added to the database.


*/data*
The file `CopiedData.csv` contains the data from Northeastern from Setpember 2,
2021 to December 10, 2021. This data was directly copied from the website while
I worked on the web-scraping program. I want to hold onto historical data. This
data can be used to test how the analysis will be conducted.


## Results
The first graph, PositiveTransmissionRate.png, shows the positive transmission 
rates between Northeastern and MA. MA consistently has a higher positive rate of 
transmission than Northeastern (>1% compared to 0.1% respectively) and shows a 
sharper increase in positive transmission rate heading into the month of November. 
Northeastern does not follow the same increase seen in the MA trend line, but 
does have a couple spikes in transmission rate while staying below 0.5%. 

The second graph, RateofChange.png, shows the rate of change of the positive 
transmission rate over time. This graph shows a lot more variability in the 
Northeastern results in the month of November. It also shows a general increase 
in transmission rates for MA.


## Discussion
From the two graphs created it seems like Northeastern is doing a better job of 
controlling the virus than the state of Massachusetts. Northeastern has been 
able to contain the virus so that the positive transmission rate never exceeds 
0.5%, which is lower than the lowest transmission rate by Massachusetts. From 
the second graph it seems like Northeastern follows a lot of the trends of 
Massachusetts, but with a couple day lag. This makes sense as it would be 
expected for an "outbreak" to occur at the state level before being seen on 
campus. This does lead into a question of whether the MA transmission rate can 
be used to predict the Northeastern transmission rate. That can be something for 
a later project to focus on.

The figure showing the number of positive tests at Northeastern University:
![Positive Tests][figures/PositiveTests.png]


## References
[1] Gojare, S., Joshi, R., &amp; Gaigaware, D. (2015). Analysis and Design of 
Selenium WebDriver Automation Testing Framework. Procedia Computer Science, 50, 
341-346. doi:https://doi.org/10.1016/j.procs.2015.04.038

[2] Parker, K. (2020, June 25). Data Science Skills: Web scraping javascript 
using python. Retrieved September 27, 2020, from
https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f

