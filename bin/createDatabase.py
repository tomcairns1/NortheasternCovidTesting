#!/usr/bin/env python3
'''
File: 
createDatabase.py

Purpose:
This script is used to create a relational database from the output file

How to Execute:
$ python3 createDatabase.py
'''

###################
# Import Libraries
###################

import pandas as pd
import sqlite3
from sqlite3 import Error


#######
# Main
#######

def main():
    ''' Business Logic '''
    # Create empty database
    db_filename = 'NUCovid.db'
    createEmptyDatabase(db_filename)

    # Import the Data
    importData(db_filename)


def createEmptyDatabase(db_filename):
    ''' 
    Fnction: createEmptyDatabase
    Parameter: db_filename (str)
    Purpose: The purpose of this function is to create a connection to a
             database file
    '''
    try:
        conn = sqlite3.connect(db_filename)
        print(f'The sqlite3 version is: {sqlite3.version}')
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def importData(db_filename):
    '''
    Function: importData
    Parameter: db_filename (str)
    Purpose: The purpose of this function is to import the data from a
             CSV file into database table
    '''
    # Hardcoding filename for now, will add to pipeline eventually
    csv_filename = '../data/output.csv'
    nucase_data = pd.read_csv(csv_filename).drop(columns=['Unnamed: 0'])

    # Import data into nucase table
    nucase_data.to_sql('nucase', con=sqlite3.Connection(db_filename),
                       if_exists='replace', index=True)


if __name__ == '__main__':
    main()
