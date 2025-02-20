"""
# YAML to CSV Converter for Bot Accounts

This script converts bot account information from a YAML file to CSV format, using JSON as an intermediate format.

## Process Flow

1. Uses `yq` to extract the 'bot_accounts' section from YAML and save as JSON
2. Loads the JSON data into a Python dictionary
3. Converts the dictionary to a pandas DataFrame
4. Reorganizes the data to include account names as a column
5. Exports the final data to CSV format

## Requirements

- Python 3.x
- Required Python packages:
  - subprocess
  - pandas
  - json
- `yq` command-line tool must be installed and accessible

## Input/Output Files

Input:
- accounts.yml: Source YAML file containing bot account information

Outputs:
- bot_accounts1.json: Intermediate JSON file
- bot_accounts1.csv: Final CSV output file

## Data Transformation

The script performs these transformations:
1. Extracts 'bot_accounts' section from YAML
2. Converts YAML structure to JSON
3. Restructures data to make account names a column
4. Reorders columns to put account name first

## Usage

Simply run the script in a directory containing the accounts.yml file:
python yaml_to_csv_converter.py

A success message will be printed when the conversion is complete.

## Note

Ensure the source YAML file is properly formatted and the 'bot_accounts' key exists
in the YAML structure.
"""

import subprocess
import pandas as pd
import json

# Run yq command to extract data from YAML and save it to a JSON file
yq_command = "yq '.bot_accounts' accounts.yml > bot_accounts1.json"
subprocess.run(yq_command, shell=True, check=True)

# Load the JSON file into a dictionary
json_file_path = 'bot_accounts1.json'
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Convert the dictionary to a DataFrame
data = pd.DataFrame.from_dict(json_data, orient='index')

# Add 'account name' column
data['account name'] = data.index

# Reorder columns to have 'account name' first
data = data.reset_index(drop=True)
data = data[['account name'] + [col for col in data.columns if col != 'account name']]

# Write the DataFrame to a CSV file
csv_file_path = 'bot_accounts1.csv'
data.to_csv(csv_file_path, index=False)

print(f"YAML data has been successfully converted to {csv_file_path}")
