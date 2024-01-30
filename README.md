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


## Data

| Country        | Code | Actual | Forecast |
|----------------|------|--------|----------|
| Austria        | AT   |        |          |
| Belgium        | BE   |  60    |  60      |
| Bulgaria       | BG   |  60    |  60      |
| Croatia        | HR   |  60    |  60      |
| Cyprus         | CY   |        |          |
| Czech Republic | CZ   |  60    |   60     |
| Denmark        | DK   |   60   |  60      |
| Estonia        | EE   |  60    |   60     |
| Finland        | FI   |  60    |   60     |
| France         | FR   |  60    |    60    |
| Germany        | DE   | 60     |   60     |
| Greece         | GR   |  60    |  60      |
| Hungary        | HU   |  15,60 |  60      |
| Italy          | IT   |   60   |    60    |
| Latvia         | LV   |   60   |  60      |
| Lithuania      | LT   |   60   |     60   |
| Luxembourg     | LU   |  15,60 |    60    |
| Malta          | MT   |        |          |
| Netherlands    | NL   |   60   |     60   |
| Poland         | PL   |  60    |    60    |
| Portugal       | PT   |   60   |   60     |
| Romania        | RO   |        |    60    |
| Slovakia       | SK   | 60     |    60    |
| Slovenia       | SI   |        |     60   |
| Spain          | ES   |        |   60     |
| Sweden         | SE   |        |   60     |
