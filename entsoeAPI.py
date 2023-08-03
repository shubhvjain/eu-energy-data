import pandas as pd
from datetime import datetime, timedelta
import time
from entsoe import EntsoePandasClient as entsoePandas
import os
import util 

DEBUG=True

def getAPIToken():
  variable_name = "ENTSOE_TOKEN"
  value = os.environ.get(variable_name)
  if value is None:
    raise ValueError(f"The required environment variable '{variable_name}' is not set.")
  return value

def entsoe_getActualGenerationDataPerProductionType(options={"country": "", "start": "", "end": ""}):
    client1 = entsoePandas(api_key=getAPIToken())
    data1 = client1.query_generation(options["country"], start=pd.Timestamp(options["start"], tz='UTC'), end=pd.Timestamp(options["end"], tz='UTC'),psr_type=None)
    
    if DEBUG:   
      fileName1= options["country"]+"-"+options["start"]+"-"+options["end"]+"-actual-raw-raw"
      data1.to_csv("./test/"+fileName1+".csv")
    
    columns_to_drop = [col for col in data1.columns if col[1] == 'Actual Consumption']
    data1['startTimeIndex'] = data1.index.strftime('%Y%m%d%H%M')
    data1['startTimeIndex'] = pd.to_datetime(data1['startTimeIndex'])
    
    duration = data1['startTimeIndex'].iloc[1] - data1['startTimeIndex'].iloc[0]
    durationMin = duration.seconds // 60

    timeStampsUTC = util.countIntervals(options["start"],options["end"],durationMin)
    
    if len(data1) == timeStampsUTC["count"]:
       data1["startTime"] = timeStampsUTC["startBin"]
       data1["endTime"] = timeStampsUTC["endBin"]
    else:
       print(options)
       raise ValueError("The length do not match.Check data manually")
        
    if DEBUG:   
      fileName= options["country"]+"-"+options["start"]+"-"+options["end"]+"-"+str(durationMin)+'-actual-raw'
      data1.to_csv("./test/"+fileName+".csv")
    
    data1 = data1.drop(columns=columns_to_drop)
    data1.columns = [(col[0] if isinstance(col, tuple) else col) for col in data1.columns]
    data1 = data1.reset_index(drop=True)
    return {"data":data1,"duration":durationMin}



def entsoe_getDayAheadAggregatedGeneration(options={"country": "", "start": "", "end": ""}):
    client = entsoePandas(api_key=getAPIToken())
    data = client.query_generation_forecast(options["country"], start=pd.Timestamp(options["start"], tz='UTC'), end=pd.Timestamp(options["end"], tz='UTC'))
    if isinstance(data,pd.Series):
        data = data.to_frame(name="Actual Aggregated")
    
    data['startTimeIndex'] = data.index.strftime('%Y%m%d%H%M')
    data['startTimeIndex'] = pd.to_datetime(data['startTimeIndex'])

    duration = data['startTimeIndex'].iloc[1] - data['startTimeIndex'].iloc[0]
    durationMin = duration.seconds // 60
    timeStampsUTC = util.countIntervals(options["start"],options["end"],durationMin)    
    data = data.head(timeStampsUTC["count"])
    data["startTime"] = timeStampsUTC["startBin"]
    data["endTime"] = timeStampsUTC["endBin"]
    
    newCol = {'Actual Aggregated': 'total'}
    data.rename(columns=newCol, inplace=True)

    if DEBUG:   
      fileName= options["country"]+"-"+options["start"]+"-"+options["end"]+"-"+str(durationMin)+'-forecast-total-raw'
      data.to_csv("./test/"+fileName+".csv")
    
    data = data.reset_index(drop=True)

    return {"data":data,"duration":durationMin}


def entsoe_getDayAheadGenerationForecastsWindSolar(options={"country": "", "start": "", "end": ""}):
    client = entsoePandas(api_key=getAPIToken())
    data = client.query_wind_and_solar_forecast(options["country"],  start=pd.Timestamp(options["start"], tz='UTC'), end=pd.Timestamp(options["end"], tz='UTC'))

    data['startTimeIndex'] = data.index.strftime('%Y%m%d%H%M')
    data['startTimeIndex'] = pd.to_datetime(data['startTimeIndex'])    

    duration = data['startTimeIndex'].iloc[1] - data['startTimeIndex'].iloc[0]
    durationMin = duration.seconds // 60

    timeStampsUTC = util.countIntervals(options["start"],options["end"],durationMin)
    data = data.head(timeStampsUTC["count"])
    data["startTime"] = timeStampsUTC["startBin"]
    data["endTime"] = timeStampsUTC["endBin"]

    validCols = ["Solar","Wind Offshore","Wind Onshore"]
    existingCol = []
    for col in validCols:
        if col in data.columns:
            existingCol.append(col)
    data["totalRenewable"] = data[existingCol].sum(axis=1)
    
    data = data.reset_index(drop=True)

    if DEBUG:   
      fileName= options["country"]+"-"+options["start"]+"-"+options["end"]+"-"+str(durationMin)+'-forecast-wind-solar-raw'
      data.to_csv("./test/"+fileName+".csv")

    return {"data":data,"duration":durationMin}


def getActualRenewableValues(options={"country":"","start":"","end":"", "interval60":True}):
    totalRaw = entsoe_getActualGenerationDataPerProductionType(options)
    total = totalRaw["data"]
    duration = totalRaw["duration"]
    if options["interval60"] == True & totalRaw["duration"] != 60 :
      print("Data will to be converted to 60 min interval")
      table = util.convertTo60MinInterval(totalRaw,options["start"],options["end"])
      duration = 60
    else: 
      table = total 
    renewableSources = ["Geothermal","Hydro Pumped Storage","Hydro Run-of-river and poundage","Hydro Water Reservoir","Marine","Other renewable","Solar","Waste","Wind Offshore","Wind Onshore"]
    windSolarOnly = ["Solar","Wind Offshore","Wind Onshore"]
    nonRenewableSources = ["Biomass","Fossil Brown coal/Lignite","Fossil Coal-derived gas","Fossil Gas","Fossil Hard coal","Fossil Oil","Fossil Oil shale","Fossil Peal","Nuclear","Other"]
    allCols = table.columns.tolist()
    renPresent  = list(set(allCols).intersection(renewableSources))
    renPresentWS  = list(set(allCols).intersection(windSolarOnly))
    nonRenPresent = list(set(allCols).intersection(nonRenewableSources))
    table["renewableTotal"] = table[renPresent].sum(axis=1)
    table["renewableTotalWS"] = table[renPresentWS].sum(axis=1)
    table["nonRenewableTotal"] = table[nonRenPresent].sum(axis=1)
    table["total"] = table["nonRenewableTotal"] + table["renewableTotal"]
    table["percentRenewable"] = ( table["renewableTotal"] / table["total"] ) * 100
    table['percentRenewable'].fillna(0, inplace=True)
    table["percentRenewable"] = table["percentRenewable"].round().astype(int)
    table["percentRenewableWS"] = ( table["renewableTotalWS"] / table["total"] ) * 100
    table['percentRenewableWS'].fillna(0, inplace=True)
    table["percentRenewableWS"] = table["percentRenewableWS"].round().astype(int)
    return {"data":table,"duration":duration}


def getRenewableForecast(options={"country": "", "start": "", "end": "" }):
    # print(options)
    totalRaw = entsoe_getDayAheadAggregatedGeneration(options)
    if totalRaw["duration"] != 60 :
        total = util.convertTo60MinInterval(totalRaw,options["start"],options["end"])
    else :
        total = totalRaw["data"]
    
    windsolarRaw = entsoe_getDayAheadGenerationForecastsWindSolar(options)
    if  windsolarRaw["duration"] != 60 :
        windsolar = util.convertTo60MinInterval(windsolarRaw,options["start"],options["end"])
    else :
        windsolar = windsolarRaw["data"]   
  
    windsolar["total"] = total["total"]
    windsolar["percentRenewable"] = (windsolar['totalRenewable'] / windsolar['total']) * 100
    windsolar['percentRenewable'].fillna(0, inplace=True)
    windsolar["percentRenewable"] = windsolar["percentRenewable"].round().astype(int)
    return {"data":windsolar,"duration":60}
