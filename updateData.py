import sys
import util as ut
import entsoeAPI as e
import pandas as pd
import carbonIntensity as ci

def updateActualDataForCountry(cname):
  """
  1. read the current data in dataframe
  2. determine the last date in the current data
  3. calculate the time interval of the new data : start time : last end_date of the last records of current data , end time  : yesterday end of day 
  4. fetch the data
  5. merge both data
  6. add additional fields
  7. save file 
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

    # now recalculating all percentage values (@TODO optimize it to recalculate vals only for new data)
    currentData = ut.calculate_energy_values(merged_df)

    # saving the file
    file = ut.DATA_folder_location+"/"+cname+"-actual-60.csv"
    currentData.to_csv(file)    
    print("done----")
  else:
    print("latest data... check tomorrow ")

def reCalculateEnergyValue(cname):
  file = ut.DATA_folder_location+"/"+cname+"-actual-60.csv"
  currentData = ut.read_actual_data_file(cname)
  print(currentData)
  # recalculate percentage 
  currentData1 = ut.calculate_energy_values(currentData)
  currentData1.to_csv(file)

def reCalcAll():
  a,f = ut.get_available_country_list()
  for ca in a:
    try:
      print(ca)
      reCalculateEnergyValue(ca)  
      print("done---")
    except Exception as e:
      print(e)



def addCarbonIntensityValueToData(cname):
  #print(1)
  file = ut.DATA_folder_location+"/"+cname+"-actual-60.csv"
  currentData = ut.read_actual_data_file(cname)
  # re-calculate percentage 
  currentData["ci1"] =  currentData.apply(lambda row: ci.calculate_carbon_intensity(row,"codecarbon1"), axis=1)
  currentData["ci2"] =  currentData.apply(lambda row: ci.calculate_carbon_intensity(row,"ipcc_min"), axis=1)
  currentData["ci3"] =  currentData.apply(lambda row: ci.calculate_carbon_intensity(row,"ipcc_mean"), axis=1)
  currentData["ci4"] =  currentData.apply(lambda row: ci.calculate_carbon_intensity(row,"ipcc_max"), axis=1)
  currentData["ci5"] =  currentData.apply(lambda row: ci.calculate_carbon_intensity(row,"eu"), axis=1)
  
  currentData.to_csv(file)


def updateAdditionalFields():
  """
  to add new fields to existing data frame and saving them in the csv file
  """
  a,f = ut.get_available_country_list()
  for ca in a:
    addCarbonIntensityValueToData(ca)


# ========================Main=================
    
def list_arguments():
    """Prints documentation for other arguments."""
    print("Available arguments:")
    for key, value in arguments_dict.items():
        print(f"{key}: {value['help']}")    


def function_one():
  """
  This method update the actual data file @TODO better doc
  """
  a,f = ut.get_available_country_list()
  for ca in a:
    updateActualDataForCountry(ca)

def function_two():
  """this method adds CI values to all data files @TODO better doc"""
  a,f = ut.get_available_country_list()
  for ca in a:
    addCarbonIntensityValueToData(ca)  

def function_three():
  print("testing")
  #updateActualDataForCountry("BE")
  # testing
  # updateData()
  # updateActualDataForCountry("BE")
  #reCalculateEnergyValue("BE")
  # reCalcAll() 
  #addCarbonIntensityValueToData("BE")
  # updateAdditionalFields()

# Define help messages and function mappings in a single dictionary
arguments_dict = {
    "0": {"help": "List all arguments", "function": list_arguments},
    "1": {"help": "Gather latest energy data (along with other calculations) and add it to the data files", "function": function_one},
    "2": {"help": "Generate carbon intensity for all data files", "function": function_two},
    "3": {"help": "test", "function": function_three},
}

def main():
    """Main function to parse arguments and execute corresponding functions."""
    if len(sys.argv) < 2 or sys.argv[1] not in arguments_dict:
        # Display usage and available arguments if no argument or invalid argument provided
        print("Usage: python script.py [argument_number]")
        print("Available arguments:")
        for key, value in arguments_dict.items():
            print(f"{key}: {value['help']}")
        return
    
    # Get argument number
    argument_number = sys.argv[1]
    
    # Execute function based on argument number
    arguments_dict[argument_number]["function"]()

if __name__ == "__main__":
    main()
