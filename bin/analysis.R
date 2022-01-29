#!/usr/bin/env Rscript

# Filename: analysis.R

# Purpose: This file is used to run the analysis for the Northeastern Covid
# Testing data and to save the created figures into the respective directory.
#///////////////////////////////////////////////////////////////////////////////

# Import the necessary files
library(tidyverse)
library(RSQLite)
library(scales)
library(lubridate)
library(tidyquant)


############
# MAIN CODE
############

# Import from the database
db <- dbConnect(SQLite(), dbname = '../data/NUCovid.db')

# Extract data
sqlCmd <- 'SELECT Date, `Positive Tests` FROM nucase;'
covid_data <- dbGetQuery(db, sqlCmd)

# Create figure
covid_data %>%
    mutate(Date = as_date(Date)) %>%
    ggplot(aes(x = Date, y = `Positive Tests`)) +
    geom_line(color = 'firebrick', group = 1) +
    theme(panel.background = element_blank(), axis.line = element_line()) +
    labs(title = 'Positive COVID-19 Tests at Northeastern University 2021 - 2022',
         y = 'Positive Tests', caption = 'Blue line represents 7 day rolling average') +
    scale_x_date(date_breaks = 'months', date_labels = '%b') +
    
    # Add moving average
    geom_ma(ma_fun = SMA, n = 7, color = 'steelblue') 

# Save the plots
ggsave('PositiveTests.png', positive_tests.figure, device = 'png',
       path = '../figures/')





