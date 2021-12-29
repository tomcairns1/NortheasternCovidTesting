#!/usr/bin/env python3
'''
Filename:
obtainMAData.py

Purpose:
This file is used to obtain and clean the data of new covid cases reported by
the state of Massachusetts. It will output the data into a file that can be
easily added to the database.

How to Execute:
$ python3 obtainMAData.py --output MAoutput.csv
'''

###################
# Import Libraries
###################

import sys
import argparse
import pandas as pd


############
# Main Code
############

def main():
    ''' Business Logic '''
    # Get command line arguments
    args = get_cli()
    print(f'The arguments are:\n{args}')

    # Make sure the output is acceptable
    if args.output == 'output.csv':
        print(f'{args.output} is already being used. Please try another filename',
              file=sys.stderr)
        sys.exit()

    # At some point here I want to add a web scraping function to download the
    # file from MA directly

    # Read in the worksheet
    ma_data = pd.read_excel(args.input, engine='openpyxl',
                            sheet_name='TestingByDate (Test Date)',
                            usecols='A, C:F, L, M, R, T')
    print(f'The data is:\n {ma_data.head()}')




def get_cli():
    '''
    Parameter: None
    Returns: cli (an instance of the command line arguments)
    Purpose: This function obtains the arguments passed into the command line
    '''
    parser = argparse.ArgumentParser(description = 'Clean MA Covid Data')

    # Add arguments
    parser.add_argument('-input', '--i', dest='input', type = str,
                        help = 'Name of file to download data into',
                        required = False,
                        default ='../data/covid-19-raw-data-12-27-2021.xlsx')

    parser.add_argument('-output', '--o', dest = 'output', type = str,
                        help = 'Name of Output File', required = False,
                        default = '../data/MAoutput.csv')

    return parser.parse_args()



if __name__ == '__main__':
    main()
