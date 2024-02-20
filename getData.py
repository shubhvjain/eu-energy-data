import pandas as pd
# to get and store data 
import entsoeAPI as e
import datetime
import time
import util as u 
# import logging
# logging.basicConfig(filename='app.log', format='%(name)s - %(levelname)s - %(message)s',level="INFO")
# TODO this code requires some changes to save files in data folder check updateDate.py

def getCountryList():
    compList1 = ["DE","FR", "BE","BG","HR","CZ","DK","EE","FI","GR","HU","IT","XK",]
    compList2 = ["LV","LT","LU","ME","NL","MK","NO","PL","PT","RO","SK","SI","ES","SE","CH"]
    # l15=["DE","HU","NL","LU"]
    return compList1 + compList2

def generateInitialFileName(options,type):
    f = options["country"]+"-"+type
    return f

def saveHistoricalActualData(options):
    fname = generateInitialFileName(options,"actual")
    try: 
        data = e.get_actual_percent_renewable(options["country"],options["start"],options["end"],options["interval60"]) 
        data.to_csv("./test/raw-"+fname+".csv")
    except Exception as error :
        print(error)

def saveHistoricalForecastData(options):
    fname = generateInitialFileName(options,"forecast")
    try: 
        data = e.get_forecast_percent_renewable(options["country"],options["start"],options["end"])
        data.to_csv("./data/"+fname+".csv")
    except Exception as error :
        print(error)


def getTestData():
    cont = getCountryList()
    for c in cont :
        print(c)
        saveHistoricalActualData({"start":"202301010000","end":"202301070000","country":c,"interval60":False})
        saveHistoricalForecastData({"start":"202301010000","end":"202301070000","country":c})
        print("====done====")

# getActualDataForAllCountries()
# getTestData()
        
def saveHistoricalActualData1(options):
    """The new method"""
    fname = generateInitialFileName(options,"actual")
    try: 
        data,duration = e.get_actual_energy_production(options["country"],options["start"],options["end"],options["interval60"])
        data = u.calculate_energy_values(data)
        data.to_csv("./data/"+fname+"-"+str(int(duration))+".csv")
    except Exception as error :
        print(error)


# saveHistoricalActualData1({"start":"202001010000","end":"202001100000","country":"DE","interval60":False})
# saveHistoricalActualData1({"start":"202001010000","end":"202312310000","country":"DE","interval60":False})