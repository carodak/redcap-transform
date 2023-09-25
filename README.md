# Redcap Transformation Script

## Overview

This Python script is designed to transform Redcap data stored in a CSV file, adding suffixes to variable names based on the associated Redcap event names. It also handles columns with no values and ensures unique 'record_id' rows in the output.

## Features

- Appends suffixes to variable names based on Redcap event names.
- Manages columns with no values.
- Generates an output CSV file with the transformed data.

## Requirements

- Python 3.x
- pandas library
- tqdm library (for progress bars)

## Installation
1. Install the required libraries:
pip install -r requirements.txt

## Usage

1. Run the script: python src/Redcap-Transform-v-X-X-X.py
2. The script will prompt you for the CSV files and display progress bars for column processing and merging. 
Note: Ensure your CSV file contains a 'redcap_event_name' column to determine suffixes.
3. The transformed data will be saved as redcap-transformed-YYYY-MM-DD_HH-MM-SS.csv in the parent directory of the root folder.

## Configuration
You can customize the list of unchangeable columns and the list of event-names->suffixes in the csv of the resources folder.

## Licence
GNU General Public License v3.0

## Author
Caroline DAKOURE
Contact: caroline.dakoure@umontreal.ca
https://linkedin.com/in/carolinedak