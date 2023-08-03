# EU Energy Data
Gathering and analyzing electricity generation data from the ENTSO-E portal.

## Setup 

1. Get API token to access ENTSOE data from https://uat-transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html
2. Add the API to the  env variable "ENTSOE_API" . 
3. Create a new conda env : `conda create --name eudata `
4. Switch to the new env : `conda activate eudata`
5. Install required packages : `conda install pandas ` ,  `python3 -m pip install entsoe-py`



## Project folder structure
- `entsoeAPI.py` : contains code to get data from ENTSOE portal using the "entsoe-py" client 
- `util.py` : contains utility functions 
- `rawData` folder : contains various types of data downloaded from different countries from the entsoe APIs
- `trainingData` folder :  contains data used to train prediction models
- `analysis` folder : some note books analyzing  downloaded data

## Usage
Todo... 