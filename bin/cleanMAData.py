#!/usr/bin/python3

'''
Filename: cleanMAData.py

Purpose: This file is used to clean the extracted csv files from the MA data.
It gets the data into a shape that is ready to be added to the database.

How to Execute: $ python3 cleanMAData.py -files <argument 1> <argument 2>
'''

import pandas as pd
import argparse

def main():
    args = get_cli()
    print(args)


def get_cli():
    '''
    Function: get_cli
    Parameters: None
    Purpose: Function to get the command line arguments
    '''
    parser = argparse.ArgumentParser(description = 'File to clean MA data')

    # Add filenames
    parser.add_argument('-files', '--f', nargs = '*', dest = 'files', 
                        help = 'Names of files', required = True)

    return parser.parse_args()


if __name__ == '__main__':
    main()