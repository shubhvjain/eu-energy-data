import pandas as pd
from datetime import datetime, timedelta
import time
from entsoe import EntsoePandasClient as entsoePandas
import os
import util 

import logging
logging.basicConfig(filename='entsoe.log', format='%(asctime)s - %(levelname)s - %(message)s',level="INFO")

DEBUG=True

def getAPIToken():
  variable_name = "ENTSOE_TOKEN"
  value = os.environ.get(variable_name)
  if value is None:
    raise ValueError(f"The required environment variable '{variable_name}' is not set.")
  return value

def entsoe_getActualGenerationDataPerProductionType(options={"country": "", "start": "", "end": ""}):
    logging.info(options)
    
    startDay = pd.Timestamp(options["start"], tz='UTC')
    endDay = pd.Timestamp(options["end"], tz='UTC')
    client1 = entsoePandas(api_key=getAPIToken())
    data1 = client1.query_generation(options["country"], start=startDay, end=endDay,psr_type=None)
    logging.info("  Fetched rows : "+str(len(data1)))

    columns_to_drop = [col for col in data1.columns if col[1] == 'Actual Consumption']
    data1 = data1.drop(columns=columns_to_drop)
    data1.columns = [(col[0] if isinstance(col, tuple) else col) for col in data1.columns]
    
    durationMin = (data1.index[1] - data1.index[0]).total_seconds() / 60
    dur = pd.Timedelta(minutes=durationMin)
    timeStampsUTC = util.countIntervals(options["start"],options["end"],durationMin)
    logging.info("  Required rows : "+str(timeStampsUTC["count"]))
    logging.info("  Duration : "+str(durationMin))
    start_time = data1.index.min()
    end_time = data1.index.max()
    expected_timestamps = pd.date_range(start=start_time, end=end_time, freq=f"{durationMin}T")
    expected_df = pd.DataFrame(index=expected_timestamps)
    missing_indices = expected_df.index.difference(data1.index)
    logging.info("  Missing values:"+str(missing_indices))
    for index in missing_indices:
      logging.info("    Missing value: "+str(index))
      rows_same_day = data1[ data1.index.date == index.date()]
      avg_val = rows_same_day.mean().fillna(0).round().astype(int)
      logging.info("      replaced with day average value of "+str(rows_same_day.index[0].date())+" : "+' '.join(avg_val.astype(str)))
      new_row = pd.DataFrame([avg_val], columns=data1.columns, index=[index])
      data1 = pd.concat([data1, new_row])            
      # prev_index = index - dur
      # next_index = index + dur
      # avg_val = (data1.loc[prev_index]+data1.loc[next_index])/2
      # logging.info("      previous value: " + ' '.join(data1.loc[prev_index].astype(str)))
      # logging.info("      previous value: " + ' '.join(data1.loc[next_index].astype(str)))
      # logging.info("      average value: " + ' '.join(avg_val.astype(str)))
      # new_row = pd.DataFrame([avg_val], columns=data1.columns, index=[index])
      # data1 = pd.concat([data1, new_row])
    data1.sort_index(inplace=True)
    
    data1["startTime"] = timeStampsUTC["startBin"]
    data1["endTime"] = timeStampsUTC["endBin"]

    if DEBUG:   
      fileName= options["country"]+"-"+options["start"]+"-"+options["end"]+"-"+str(durationMin)+'-actual-raw'
      data1.to_csv("./test/"+fileName+".csv")
    
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
    if options["interval60"] == True and totalRaw["duration"] != 60.0 :
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
