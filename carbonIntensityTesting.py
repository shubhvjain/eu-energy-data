
# # comparing carbon intensity values


import pandas as pd
import util as ut
import numpy as np
import json
from datetime import datetime
clist = ["BE","DE","FR","FI","GR","LT","NL","NO","PL"]


'''
for a given country  and column name 
- read exp data from data folder 
- read ref data : multiple files combine data
'''
def combine_data_files1(country):
    # Read the three CSV files
    df1 = pd.read_csv('./testdata/'+country+'_2021_hourly.csv')
    df2 = pd.read_csv('./testdata/'+country+'_2022_hourly.csv')
    df3 = pd.read_csv('./testdata/'+country+'_2023_hourly.csv')
    # Concatenate the DataFrames
    combined_df = pd.concat([df1, df2, df3])
    # Optionally reset the index
    combined_df = combined_df.reset_index(drop=True)
    # Save the combined DataFrame to a new CSV file
    combined_df.to_csv('./testdata/'+country+'_2021_2023_hourly.csv', index=False)
    for c in clist:
        combine_data_files1(c)

def get_combined_data(country):
    exp_file = "./data/"+country+"-actual-60.csv"
    ref_file = "./testdata/"+country+"_2021_2023_hourly.csv"
    exp = pd.read_csv(exp_file)
    exp['startTime1'] = pd.to_datetime(exp['startTime'], format = '%Y%m%d%H%M')
    exp1 =  exp[(exp['startTime1'].dt.year >= 2021) & (exp['startTime1'].dt.year <= 2023)]
    ref = pd.read_csv(ref_file)
    ref['startTime1'] = pd.to_datetime(ref['Datetime (UTC)'])
    ref.set_index('startTime1', inplace=True)
    exp.set_index('startTime1', inplace=True)
    combined_data = pd.concat([ref.loc['2021-01-01':'2023-12-31'], exp.loc['2021-01-01':'2023-12-31']], axis=1)
    combined_data.rename(columns={"Carbon Intensity gCO₂eq/kWh (direct)":"ci_electmap"}, inplace=True)
    return combined_data


def make_comparisons(country):
    df = get_combined_data(country)
    comparison = {}

    # ci1 with elect map data
    squared_diff_ci1 = (df['ci1'] - df['ci_electmap']) ** 2
    mean_squared_diff_ci1 = np.mean(squared_diff_ci1)
    rmse_ci1 = np.sqrt(mean_squared_diff_ci1)
    comparison["rmse_ci1_and_ci_electmap_direct"] = rmse_ci1
    mae_ci1 = np.mean(np.abs(df['ci_electmap'] - df['ci1']))
    comparison["mae_ci1_and_ci_electmap"] = mae_ci1

    # ci3 with elect map
    squared_diff_ci3 = (df['ci3'] - df['ci_electmap']) ** 2
    mean_squared_diff_ci3 = np.mean(squared_diff_ci3)
    rmse_ci3 = np.sqrt(mean_squared_diff_ci3)
    comparison["rmse_ci3_and_ci_electmap_direct"] = rmse_ci3
    mae_ci3 = np.mean(np.abs(df['ci_electmap'] - df['ci3']))
    comparison["mae_ci3_and_ci_electmap"] = mae_ci3

    # ci5 with elect map 
    squared_diff_ci5 = (df['ci5'] - df['ci_electmap']) ** 2
    mean_squared_diff_ci5 = np.mean(squared_diff_ci5)
    rmse_ci5 = np.sqrt(mean_squared_diff_ci5)
    comparison["rmse_ci5_and_ci_electmap_direct"] = rmse_ci5
    mae_ci5 = np.mean(np.abs(df['ci_electmap'] - df['ci5']))
    comparison["mae_ci5_and_ci_electmap"] = mae_ci5

   # comparing percentage renewable values
    squared_diff_ci2 = (df['percentRenewable'] - df['Renewable Percentage']) ** 2
    mean_squared_diff_ci2 = np.mean(squared_diff_ci2)
    rmse_ci2 = np.sqrt(mean_squared_diff_ci2)
    comparison["rmse_per_renew_and_pre_renew_electmap"] = rmse_ci2  
    mae_perre = np.mean(np.abs(df['Renewable Percentage'] - df['percentRenewable']))
    comparison["mae_per_renew_and_pre_renew_electmap"] = mae_perre
    
    comparison["update_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # print(comparison)
    comparison["country"] = country
    with open('./data/'+country+'-comparison.json', 'w') as f:
        json.dump(comparison, f, indent=4)
    

for c in clist:
   make_comparisons(c)

