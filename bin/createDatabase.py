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


def createEmptyDatabase(db_filename):
    ''' 
    Fnction: createEmptyDatabase
    Parameter: db_filename (str)
    Purpose: The purpose of this function is to create a connection to a
             database file
    '''
    try:
        conn = sqlite3.connect(db_filename)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()