#!/bin/sqlite3
/*
Filename:
createDatabase.sql

Purpose:
This script is used to create a database to contain the Northeastern Covid Data
*/

-- Drop tables if they exist
DROP TABLE IF EXISTS nucase;
DROP TABLE IF EXISTS macase;

-- Add tables
CREATE TABLE nucase (
    pk INT NOT NULL,
    test_date DATE,
    total_tests INT,
    negative_tests INT,
    negative_rate VARCHAR(255),
    positive_tests INT,
    positive_rate VARCHAR(255),
    rate_of_change FLOAT,
    PRIMARY KEY (pk)
);

CREATE TABLE macase (
    pk INT NOT NULL,
    test_date DATE,
    positive_rate VARCHAR(255),
    PRIMARY KEY (pk)
);
