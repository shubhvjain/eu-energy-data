import pandas as pd

# ====================== Generation ===========================
"""
remember , 
1 kg = 1000 grams
1MWh = 1000 kWh 
this means,
1 kg/MWh = 1 kg/(kWh * 1000 ) 
         = 1000 g/ (kWH * 1000) ....(both 1000 cancel each other out)
=> 1kg/MWh = 1g/kWh         
"""


def method_codecarbon1(row):
    # https://mlco2.github.io/codecarbon/methodology.html#carbon-intensity
    # base values in kg/MWh 
    base_carbon_intensity = {
        "Coal": 995,
        "Petroleum": 816,
        "Natural Gas":743,
        "Geothermal":38,
        "Hydroelectricity":26,
        "Nuclear":29,
        "Solar":48,
        "Wind":26
    }
    # calculate percentage
    result = (base_carbon_intensity["Coal"] * row["Coal_per"]
        + base_carbon_intensity["Geothermal"] * row["Geothermal_per"]
        + base_carbon_intensity["Hydroelectricity"] * row["Hydroelectricity_per"]
        + base_carbon_intensity["Natural Gas"] * row["Natural Gas_per"]
        + base_carbon_intensity["Nuclear"] * row["Nuclear_per"]
        + base_carbon_intensity["Petroleum"] * row["Petroleum_per"]
        + base_carbon_intensity["Solar"] * row["Solar_per"]
        + base_carbon_intensity["Wind"] * row["Wind_per"] )/100
    return round(result, 2)


"""
IPCC values
| type        | average of                                                  | min  | mean | max  |
|-------------|-------------------------------------------------------------|------|------|------|
| coal        | Coal—PC                                                     | 740  | 820  | 910  |
| natural gas | Gas—Combined Cycle                                          | 410  | 490  | 650  |
| biogas      | Biomass—cofiring,Biomass—dedicated                          | 375  | 485  | 655  |
| geothermal  | Geothermal                                                  | 6    | 38   | 79   |
| hydropower  | Hydropower                                                  | 1    | 24   | 2200 |
| nuclear     | Nuclear                                                     | 3.7  | 12   | 110  |
| solar       | Concentrated Solar Power, Solar PV—rooftop,Solar PV—utility | 17.6 | 38.6 | 101  |
| wind        | Wind onshore, Wind offshore                                 | 7.5  | 11.5 | 45.5 |

https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_annex-iii.pdf#page=7

"""

def method_ipcc_lifecycle_min(row):
    # https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_annex-iii.pdf#page=7 (using min values)
    min_carbon_intensity = {
        "Coal": 740, 
        "Natural Gas":410,
        "Biomass":375,
        "Geothermal":6,
        "Hydroelectricity":1,
        "Nuclear":3.7,
        "Solar":17.6, 
        "Wind":7.5 
    }
    # calculate percentage
    result = (min_carbon_intensity["Coal"] * row["Coal_per"]
        + min_carbon_intensity["Geothermal"] * row["Geothermal_per"]
        + min_carbon_intensity["Hydroelectricity"] * row["Hydroelectricity_per"]
        + min_carbon_intensity["Natural Gas"] * row["Natural Gas_per"]
        + min_carbon_intensity["Nuclear"] * row["Nuclear_per"]
        + min_carbon_intensity["Solar"] * row["Solar_per"]
        + min_carbon_intensity["Biomass"] * row["Biomass_per"] 
        + min_carbon_intensity["Wind"] * row["Wind_per"] )/100
    return round(result, 2)


def method_ipcc_lifecycle_mean(row):
    # https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_annex-iii.pdf#page=7 (using mean values)
    mean_carbon_intensity = {
        "Coal": 820, 
        "Biomass": 485,
        "Natural Gas":490,
        "Geothermal":38,
        "Hydroelectricity":24,
        "Nuclear":12,
        "Solar":38.6,
        "Wind":11.5 
    }
    # calculate percentage
    result = (mean_carbon_intensity["Coal"] * row["Coal_per"]
        + mean_carbon_intensity["Geothermal"] * row["Geothermal_per"]
        + mean_carbon_intensity["Hydroelectricity"] * row["Hydroelectricity_per"]
        + mean_carbon_intensity["Natural Gas"] * row["Natural Gas_per"]
        + mean_carbon_intensity["Nuclear"] * row["Nuclear_per"]
        + mean_carbon_intensity["Solar"] * row["Solar_per"]
        + mean_carbon_intensity["Wind"] * row["Wind_per"]
        + mean_carbon_intensity["Biomass"] * row["Biomass_per"] 

          )/100
    return round(result, 2)

def method_ipcc_lifecycle_max(row):
    # https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_annex-iii.pdf#page=7 (using mean values)
    max_carbon_intensity = {
        "Coal": 910, 
        "Biomass": 655,
        "Natural Gas":650,
        "Geothermal":79,
        "Hydroelectricity":2200,
        "Nuclear":110,
        "Solar":101,
        "Wind":45.5 
    }
    # calculate percentage
    result = (max_carbon_intensity["Coal"] * row["Coal_per"]
        + max_carbon_intensity["Geothermal"] * row["Geothermal_per"]
        + max_carbon_intensity["Hydroelectricity"] * row["Hydroelectricity_per"]
        + max_carbon_intensity["Natural Gas"] * row["Natural Gas_per"]
        + max_carbon_intensity["Nuclear"] * row["Nuclear_per"]
        + max_carbon_intensity["Solar"] * row["Solar_per"]
        + max_carbon_intensity["Wind"] * row["Wind_per"] 
        + max_carbon_intensity["Biomass"] * row["Biomass_per"] 

        )/100
    return round(result, 2)

def method_EU_paper(row):
    # based on N. Scarlat, M. Prussi, and M. Padella, ‘Quantification of the carbon intensity of electricity produced and used in Europe’, Applied Energy, vol. 305, p. 117901, Jan. 2022, doi: 10.1016/j.apenergy.2021.117901.
    # fig 9
    base_carbon_intensity = {
        "Coal": 970,  # sold fuels
        "Petroleum": 790 ,# oil
        "Biomass": 65, 
        "Natural Gas":425,
        "Geothermal":38,
        "Hydroelectricity":19,
        "Nuclear":24,
        "Solar":40,
        "Wind":11 
    }
    result = (base_carbon_intensity["Coal"] * row["Coal_per"]
        + base_carbon_intensity["Biomass"] * row["Biomass_per"]
        + base_carbon_intensity["Geothermal"] * row["Geothermal_per"]
        + base_carbon_intensity["Hydroelectricity"] * row["Hydroelectricity_per"]
        + base_carbon_intensity["Natural Gas"] * row["Natural Gas_per"]
        + base_carbon_intensity["Nuclear"] * row["Nuclear_per"]
        + base_carbon_intensity["Petroleum"] * row["Petroleum_per"]
        + base_carbon_intensity["Solar"] * row["Solar_per"]
        + base_carbon_intensity["Wind"] * row["Wind_per"] )/100
    return round(result, 2) 
    

def calculate_carbon_intensity(row, methodType):
    '''
    '''
    methods = {
        "codecarbon1":method_codecarbon1,
        "ipcc_min":method_ipcc_lifecycle_min,
        "ipcc_mean":method_ipcc_lifecycle_mean,
        "ipcc_max":method_ipcc_lifecycle_mean,
        "eu":method_EU_paper
    }
    return methods[methodType](row)
    