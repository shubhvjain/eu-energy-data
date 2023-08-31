# to get and store data 
import entsoeAPI as e
import datetime
import time
import logging
logging.basicConfig(filename='app.log', format='%(name)s - %(levelname)s - %(message)s',level="INFO")

def optionToFile(opt):
    f = opt["country"]+"-"+opt["start"]+"-"+opt["end"]
    return f
    

def getCountryList():
    compList1 = ["DE","FR", "BE","BG","HR","CZ","DK","EE","FI","GR","HU","IT","XK",]
    compList2 = ["LV","LT","LU","ME","NL","MK","NO","PL","PT","RO","SK","SI","ES","SE","CH"]
    # l15=["DE","HU","NL","LU"]
    return compList2

def generateIntialFileName(options,type):
    f = options["country"]+"-"+options["start"]+"-"+options["end"]+"-"+type
    return f

def saveHistoricalActualData(options):
    fname = generateIntialFileName(options,"actual")
    try: 
        data = e.get_actual_percent_renewable(options["country"],options["start"],options["end"],True) 
        data.to_csv("./rawData1/"+fname+".csv")
    except Exception as error :
        print(error)

def saveHistoricalForecastData(options):
    fname = generateIntialFileName(options,"forecast")
    try: 
        data = e.get_forecast_percent_renewable(options["country"],options["start"],options["end"])
        data.to_csv("./rawData1/"+fname+".csv")
    except Exception as error :
        print(error)


def getTestData():
    cont = getCountryList()
    for c in cont :
        print(c)
        saveHistoricalActualData({"start":"202301010000","end":"202304010000","country":c,"interval60":True})
        saveHistoricalForecastData({"start":"202301010000","end":"202304010000","country":c})
        print("====done====")

# getActualDataForAllCountries()



getTestData()