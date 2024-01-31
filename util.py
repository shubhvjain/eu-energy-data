import os
from datetime import datetime
import pandas as pd

EU_country_codes = [
    "AT",  # Austria
    "BE",  # Belgium
    "BG",  # Bulgaria
    "CY",  # Cyprus
    "CZ",  # Czech Republic
    "DE",  # Germany
    "DK",  # Denmark
    "EE",  # Estonia
    "ES",  # Spain
    "FI",  # Finland
    "FR",  # France
    "GR",  # Greece
    "HR",  # Croatia
    "HU",  # Hungary
    "IE",  # Ireland
    "IT",  # Italy
    "LT",  # Lithuania
    "LU",  # Luxembourg
    "LV",  # Latvia
    "MT",  # Malta
    "NL",  # Netherlands
    "PL",  # Poland
    "PT",  # Portugal
    "RO",  # Romania
    "SE",  # Sweden
    "SI",  # Slovenia
    "SK",  # Slovakia
]

DATA_folder_location= "data"


def get_available_country_list(data_folder="data"):
    """
    Generate lists of country codes for actual and forecast data from CSV filenames in the data folder.

    Parameters:
    data_folder (str): The path to the folder containing the CSV files.

    Returns:
    tuple: A tuple containing two lists:
        - countryActual (list): List of country codes for actual data.
        - countryForecast (list): List of country codes for forecast data.
    """
    countryActual = []
    countryForecast = []

    # Function to extract country code and data type from file name
    def extract_info(filename):
        parts = filename.split('-')
        country_code = parts[0]
        data_type = parts[1]
        return country_code, data_type

    # Iterate over files in the data folder
    for filename in os.listdir(data_folder):
        if filename.endswith(".csv") and filename.endswith("-60.csv"):
            country_code, data_type = extract_info(filename)
            if data_type == "actual":
                countryActual.append(country_code)
            elif data_type == "forecast":
                countryForecast.append(country_code)

    return countryActual, countryForecast


def get_today_starting_date():
    # Get today's date
  today = datetime.today()
  # Format the date in yyyymmddhhmm format
  formatted_date = today.strftime("%Y%m%d") + "0000"
  return formatted_date



def read_actual_data_file(ccode):
  file = DATA_folder_location+"/"+ccode+"-actual-60.csv"
  currentData = pd.read_csv(file)
  currentData = currentData.drop(currentData.columns[0], axis=1)
  # currentData['startTime'] = currentData['startTime'].astype(str)
  # currentData['endTime'] = currentData['endTime'].astype(str)
  currentData['startTime'] = pd.to_datetime(currentData['startTime'], format='%Y%m%d%H%M')
  currentData['endTime'] = pd.to_datetime(currentData['endTime'], format='%Y%m%d%H%M')
  currentData['startTime'] = currentData['startTime'].dt.strftime('%Y%m%d%H%M')
  currentData['endTime'] = currentData['endTime'].dt.strftime('%Y%m%d%H%M')
  return currentData