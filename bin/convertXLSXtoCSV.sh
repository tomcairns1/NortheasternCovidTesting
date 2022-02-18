#!/usr/bin/env bash

# Filename: convertXLSXtoCSV

# Purpose: This file is to take the downloaded MA data excel file and convert
# the single spreadsheet into a csv file.

# Find the filename
FILENAME=../data/*.xlsx
echo $FILENAME

# Extract the weekly city report. 
xlsx2csv $FILENAME -s 26 -f "%m/%d/%Y" > ../data/weeklyCityReport.csv
echo "1st file converted"
# Extract the testing by date
xlsx2csv $FILENAME -s 24 > ../data/MATestingByDate.csv
echo "2nd file converted"

