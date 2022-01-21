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


############
# MAIN CODE
############

# Import from the database
db <- dbConnect(SQLite(), dbname = '../data/NUCovid.db')

# Extract data
sqlCmd <- 'SELECT Date, `Positive Tests` FROM nucase;'
covid_data <- dbGetQuery(db, sqlCmd)

# Create figure
positive_tests.figure <- covid_data %>%
    mutate(Date = as_date(Date)) %>%
    ggplot() +
    geom_line(aes(x = Date, y = `Positive Tests`), color = 'firebrick',
              group = 1) +
    theme(panel.background = element_blank(), axis.line = element_line()) +
    labs(title = 'Positive COVID-19 Tests at Northeastern University 2021 - 2022',
         y = 'Positive Tests') +
    scale_x_date(date_breaks = 'months', date_labels = '%b')

# Save the plots
ggsave('PositiveTests.png', positive_tests.figure, device = 'png',
       path = '../figures/')





