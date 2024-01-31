import util as ut
import entsoeAPI as e
import pandas as pd

def updateData():
  """
  1. get a list of countries for which data is available (actual, forecast)
  2. for each country in actual, update actual data 
  3. for each country in forecast, update forecast data
  """
  a,f = ut.get_available_country_list()
  for ca in a:
    updateActualDataForCountry(ca)
  # for cf in f :
  #   updateForecastDataForCountry(cf)


def updateActualDataForCountry(cname):
  """
  1. read the current data in dataframe
  2. determine the last date in the current data
  3. calculate the time interval of the new data : start time : last end_date of the last records of current data , end time  : yesterday end of day 
  4. fetch the data
  5. merge both data
  6. save file 
  """
  currentData = ut.read_actual_data_file(cname)
  lastEndDate = str(currentData.iloc[-1]["endTime"])
  todayDate = ut.get_today_starting_date()
  # temp = "202301310000"
  # todayDate = temp
  if lastEndDate != todayDate :
    print(cname)
    print(lastEndDate)
    print(todayDate)
    newData = e.get_actual_percent_renewable(cname,lastEndDate,todayDate,True) 
    newData = newData.rename(columns={'startTimeUTC': 'startTime'})
    # Convert string columns to datetime format
    newData['startTime'] = pd.to_datetime(newData['startTime'], format='%Y%m%d%H%M')
    # Add 60 minutes to startDate and convert back to string format
    newData['endTime'] = (newData['startTime'] + pd.Timedelta(minutes=60)).dt.strftime('%Y%m%d%H%M')
    newData['startTime'] = newData['startTime'].dt.strftime('%Y%m%d%H%M')
    merged_df = pd.merge(currentData, newData, how='outer')
    file = ut.DATA_folder_location+"/"+cname+"-actual-60.csv"
    merged_df.to_csv(file)
    #print(newData)
    print("done----")
  else:
     print("latest data... check tomorrow ")


def updateForecastDataForCountry(cname):
  file = ut.DATA_folder_location+"/"+cname+"-forecast-60.csv"
  print(file)  


updateData()
# updateActualDataForCountry("BE")
