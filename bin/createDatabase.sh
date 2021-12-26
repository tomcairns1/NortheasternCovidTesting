#!/bin/bash

# Filename:
# createDatabase.sh

# Purpose:
# This file creates the database from the sql file. 

# How to Execute:
# bash createDatabase.sh

# Create the database
sqlite3 NUCovid.db '.read createDatabase.sql'


