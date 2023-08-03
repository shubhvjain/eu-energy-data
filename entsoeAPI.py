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
       raise ValueError("The length do not match.Check data manually")
        
    if DEBUG:   
      fileName= options["country"]+"-"+options["start"]+"-"+options["end"]+"-"+str(durationMin)+'-raw'
      data1.to_csv("./test/"+fileName+".csv")
    
    data1 = data1.drop(columns=columns_to_drop)
    data1.columns = [(col[0] if isinstance(col, tuple) else col) for col in data1.columns]
    data1 = data1.reset_index(drop=True)
    return data1


def getActualRenewableValues(options={"country":"","start":"","end":"", "interval60":True}):
    totalRaw = entsoe_getActualGenerationDataPerProductionType(options)
    total = totalRaw
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
    return table
