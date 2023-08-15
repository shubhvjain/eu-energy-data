import entsoeAPI as e
import pandas as pd
from entsoe import EntsoePandasClient as entsoePandas
from entsoe import EntsoeRawClient as eRaw
import os

def generateIntialFileName(options,type):
    f = options["country"]+"-"+options["start"]+"-"+options["end"]+"-"+type
    return f

def saveHistoricalActualData(options):
    fname = generateIntialFileName(options,"actual")
    try: 
        #logging.info("[Start] Getting : "+ fname)
        #start_time = time.time()
        data = e.getActualRenewableValues(options)
        #end_time = time.time()
        #time_taken = end_time - start_time
        fname = fname+"-"+str(data["duration"])
        #logging.info("[Stop] Getting : "+ fname+" ; Took : "+str(round(time_taken,2))+" s")
        data["data"].to_csv("./rawData/"+fname+".csv")
    except Exception as error :
        print(error)
        #logging.error("[Stop][Error] Getting :"+fname,exc_info=True)


# saveHistoricalActualData({"start":"202204010000","end":"202204200000","country":"FR","interval60":True})
# saveHistoricalActualData({"start":"202201010000","end":"202301010000","country":"FR","interval60":True})

def getAPIToken():
  variable_name = "ENTSOE_TOKEN"
  value = os.environ.get(variable_name)
  if value is None:
    raise ValueError(f"The required environment variable '{variable_name}' is not set.")
  return value


def checkActualFranc():
    oneDay = pd.Timedelta(days=1)
    #endDayPlus1 = pd.Timestamp(options["end"], tz='UTC') + oneDay
    client1 = entsoePandas(api_key=getAPIToken())
    data1 = client1.query_generation("FR", start=pd.Timestamp("202204150000", tz='UTC'), end=pd.Timestamp("202204170000", tz='UTC'),psr_type=None)
    data1.to_csv("./manualDownloads/france2022-actual-entsoe-py.csv")
    # data2 = client1.query_generation("FR", start=pd.Timestamp("202201010000",tz="Europe/Berlin"), end=pd.Timestamp("202301010000",tz="Europe/Berlin"),psr_type=None)
    # data2.to_csv("./manualDownloads/test/france2022-actual-entsoe-1.csv")
    
def check1():
    client = eRaw(api_key=getAPIToken())
    xml_string = client.query_generation("FR", start=pd.Timestamp("202204160000", tz='UTC'), end=pd.Timestamp("202204170000", tz='UTC'))
    with open('outfile.xml', 'w') as f:
      f.write(xml_string)

# check1()

# checkActualFranc()

def checkValueFrance2022():
    manual = pd.read_csv("./manualDownloads/test/FR-1.csv")
    api = pd.read_csv("./manualDownloads/test/FR-2.csv")
    result = pd.concat([manual, api], axis=1)
    result.to_csv("./manualDownloads/test/france2022-actual-final.csv")


# checkValueFrance2022()

# data = e.entsoe_getActualGenerationDataPerProductionType({"country":"FR","start":"202204150000","end":"202204170000"})
# print(data)

# data = e.entsoe_getDayAheadAggregatedGeneration({"start":"202305010000","end":"202305150000","country":"FR","interval60":False})
# print(data)

# data1 = e.entsoe_getDayAheadGenerationForecastsWindSolar({"start":"202007010000","end":"202007250000","country":"FR","interval60":False})
# print(data1["data"])
# data1["data"].to_csv("./test/sample.csv")
# data1 = e.entsoe_getDayAheadGenerationForecastsWindSolar({"start":"202004040000","end":"202004060000","country":"LV","interval60":True})
# print(data1)

# data1 = e.getRenewableForecast({"start":"202305100000","end":"202305200000","country":"GR","interval60":True})
# print(data1)



# def refineData(options,data1):
#   durationMin = (data1.index[1] - data1.index[0]).total_seconds() / 60
#   timeStampsUTC = util_countIntervals(options["start"],options["end"],durationMin)

#   logging.info("  Row count : Fetched =  "+str(len(data1))+" , Required = "+str(timeStampsUTC["count"]))
#   logging.info("  Duration : "+str(durationMin))
#   totalAverageValue = data1.mean().fillna(0).round().astype(int)

#   data1['startTimeIndex'] = data1.index.strftime('%Y%m%d%H%M')
#   data1['startTimeIndex'] = pd.to_datetime(data1['startTimeIndex'])
#   data1.to_csv("./test/"+"testrefine1"+".csv")
#   start_time = data1.index.min()
#   end_time = data1.index.max()
#   expected_timestamps = pd.date_range(start=start_time, end=end_time, freq=f"{durationMin}T")
#   expected_df = pd.DataFrame(index=expected_timestamps)
#   missing_indices = expected_df.index.difference(data1.index)
#   logging.info("  Missing values ("+str(len(missing_indices))+") :"+str(missing_indices))
#   for index in missing_indices:
#     logging.info("    Missing value: "+str(index))
#     rows_same_day = data1[ data1.index.date == index.date()]    
#     if len(rows_same_day)>0 :
#       avg_val = rows_same_day.mean().fillna(0).round().astype(int)
#       avg_type = "average day value "+ str(rows_same_day.index[0].date())+" "
#     else:
#       avg_val = totalAverageValue
#       avg_type = "whole data average "
#     logging.info("      replaced with "+avg_type+" : "+' '.join(avg_val.astype(str)))
#     new_row = pd.DataFrame([avg_val], columns=data1.columns, index=[index])
#     data1 = pd.concat([data1, new_row])            
#     # prev_index = index - dur
#     # next_index = index + dur
#     # avg_val = (data1.loc[prev_index]+data1.loc[next_index])/2
#     # logging.info("      previous value: " + ' '.join(data1.loc[prev_index].astype(str)))
#     # logging.info("      previous value: " + ' '.join(data1.loc[next_index].astype(str)))
#     # logging.info("      average value: " + ' '.join(avg_val.astype(str)))
#     # new_row = pd.DataFrame([avg_val], columns=data1.columns, index=[index])
#     # data1 = pd.concat([data1, new_row])
#   data1.sort_index(inplace=True)
#   data1.to_csv("./test/"+"testrefine2"+".csv")
#   print(data1)
#   d = pd.DataFrame({"start": timeStampsUTC["startBin"] ,"end": timeStampsUTC["endBin"]})
#   d.to_csv("./test/datetest.csv")
#   data1["startTime"] = timeStampsUTC["startBin"]
#   data1["endTime"] = timeStampsUTC["endBin"]
#   return data1