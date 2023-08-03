# to get and store data 
import entsoeAPI as e
import datetime
import time
import logging
logging.basicConfig(filename='app.log', format='%(name)s - %(levelname)s - %(message)s',level="INFO")

def optionToFile(opt):
    f = opt["country"]+"-"+opt["start"]+"-"+opt["end"]
    return f

def test():
    option1 = {"start":"202301010000","end":"202301020000","country":"DE"}
    option2 = {"start":"202301010000","end":"202303010000","country":"DE"}
    option3 = {"start":"202301010000","end":"202303010000","country":"ES"}
    option4 = {"start":"202301010000","end":"202303010000","country":"GR"}
    option5 = {"start":"202301010000","end":"202301050000","country":"DE","interval60":True}
    option6 = {"start":"202301010000","end":"202301050000","country":"DE","interval60":False}
    option7 = {"start":"202301010000","end":"202301050000","country":"ES","interval60":True}
    option8 = {"start":"202301010000","end":"202301050000","country":"ES","interval60":False}
    # test1 = e.getActualRenewableValues(option7)
    # test1["data"].to_csv("./test/"+optionToFile(option7)+"-"+str(test1["duration"])+".csv")
    # test2 = e.getActualRenewableValues(option8)
    # test2["data"].to_csv("./test/"+optionToFile(option8)+"-"+str(test2["duration"])+".csv")
    # a = e.getActualRenewableValues(option1)
    # a.to_csv("./test/"+optionToFile(option1)+".csv")
    # b = e.getActualRenewableValues(option2)
    # b.to_csv("./test/"+optionToFile(option2)+".csv")
    # t1 = e.entsoe_getDayAheadAggregatedGeneration(option1)
    # t1 = e.entsoe_getDayAheadAggregatedGeneration(option1)
    # t1 = e.entsoe_getDayAheadAggregatedGeneration(option2)
    #t2 = e.entsoe_getDayAheadGenerationForecastsWindSolar(option2)
    #t3 = e.entsoe_getDayAheadGenerationForecastsWindSolar(option3)
    # ct = getCountryList()
    # for c in ct :
    #     print()        
    # test3 = e.getRenewableForecast(option5)
    # test3["data"].to_csv("./test/"+optionToFile(option5)+"-forecast-"+str(test3["duration"])+".csv")
    # test4 = e.getRenewableForecast(option6)
    # test4["data"].to_csv("./test/"+optionToFile(option6)+"-forecast-"+str(test4["duration"])+".csv")


"""
Getting historical data for selected countries from 1-Jan-2020 to 30-June-2023
Type of data to gather :
- Histrical actual generation data (+ percentage of renewable energy) in 60 min interval
- Histrical actual generation data (+ percentage of renewable energy) in orignal interval (if not reported in 60 min interval)
- Historical forecast data (in 60 min interval) 

All this data is stored automatically in the "rawData" folder. 
File name format : "countryname-startDate-endData-interval-type.csv" (type is either: "actual" or "forcast")
 
"""

def getCountryList():
    compList = ["DE","FR", "BE","BG","HR","CZ","DK","EE","FI","FR","GR","HU","IT","XK","LV","LT","LU","ME","NL","MK","NO","PL","PT","RO","SK","SI","ES","SE","CH"]
    return compList

def generateIntialFileName(options,type):
    f = options["country"]+"-"+options["start"]+"-"+options["end"]+"-"+type
    return f

def saveHistoricalActualData(options):
    fname = generateIntialFileName(options,"actual")
    try: 
        logging.info("[Start] Getting : "+ fname)
        start_time = time.time()
        data = e.getActualRenewableValues(options)
        end_time = time.time()
        time_taken = end_time - start_time
        fname = fname+"-"+str(data["duration"])
        logging.info("[Stop] Getting : "+ fname+" ; Took : "+str(round(time_taken,2))+" s")
        data["data"].to_csv("./rawData/"+fname+".csv")
    except Exception as error :
        logging.error("[Stop][Error] Getting :"+fname,exc_info=True)

def saveHistoricalForecastData(options):
    fname = generateIntialFileName(options,"forecast")
    try: 
        logging.info("[Start] Getting : "+ fname)
        start_time = time.time()
        data = e.getRenewableForecast(options)
        end_time = time.time()
        time_taken = end_time - start_time
        fname = fname+"-"+str(data["duration"])
        logging.info("[Stop] Getting : "+ fname+" ; Took : "+str(round(time_taken,2))+" s")
        data["data"].to_csv("./rawData/"+fname+".csv")
    except Exception as error :
        logging.error("[Stop][Error] Getting :"+fname,exc_info=True)


# saveHistoricalForecastData({"start":"202301010000","end":"202301050000","country":"DE"})
# saveHistoricalActualData({"start":"202301010000","end":"202301050000","country":"DE","interval60":False})
# saveHistoricalActualData({"start":"202301010000","end":"202301050000","country":"DE","interval60":True})