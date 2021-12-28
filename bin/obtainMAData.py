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

import pandas as pd
import argparse

############
# Main Code
############

def main():
    ''' Business Logic '''
    # Get command line arguments
    args = get_cli()

    # Make sure the output is acceptable
    



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
                        required = False)
    
    parser.add_argument('-output', '--o', dest = 'output', type = str,
                        help = 'Name of Output File', required = False,
                        default = '../data/MAoutput.csv')

    return parser.parse_args()



if __name__ == '__main__':
    main()

