# to get and store data 
import entsoeAPI as e

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


test()

def getCountryList():
    compList = ["DE","FR", "BE","BG","HR","CZ","DK","EE","FI","FR","GR","HU","IT","XK","LV","LT","LU","ME","NL","MK","NO","PL","PT","RO","SK","SI","ES","SE","CH"]
    return compList

def saveDataForOriginalInterval(opt):
    print()

def saveDataFor60Minterval(opt):
    print()

