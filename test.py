import entsoeAPI as e
import pandas as pd

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




# To verfiy if the data download is correct 
"""
Country 1 : France. Data for 2020 downloaded manually from the ENTSOE portal

"""
from entsoe import EntsoePandasClient as entsoePandas
from entsoe import EntsoeRawClient as eRaw
import os

def getAPIToken():
  variable_name = "ENTSOE_TOKEN"
  value = os.environ.get(variable_name)
  if value is None:
    raise ValueError(f"The required environment variable '{variable_name}' is not set.")
  return value


def checkActualFranc():
    #print(options)
    #print(pd.Timestamp(options["start"], tz='UTC'))
    #print(pd.Timestamp(options["end"], tz='UTC'))
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