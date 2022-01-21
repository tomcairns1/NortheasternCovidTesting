#!/usr/bin/env bash

# pipeline.sh

# This file is used to run the Northeastern Covid Testing pipeline.

# Run the pipeline
# NEED TO UPDATE WITH FILENAMES
python3 NortheasternCovidWebScraper.py | bash createDatabase.sh | Rscript analysis.R
