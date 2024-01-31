import pandas as pd


def method_codecarbon1(row):
    # https://mlco2.github.io/codecarbon/methodology.html#carbon-intensity
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
    # calcuate perentage
    result = (base_carbon_intensity["Coal"] * row["Coal_per"]
        + base_carbon_intensity["Geothermal"] * row["Geothermal_per"]
        + base_carbon_intensity["Hydroelectricity"] * row["Hydroelectricity_per"]
        + base_carbon_intensity["Natural Gas"] * row["Natural Gas"]
        + base_carbon_intensity["Nuclear"] * row["Nuclear_per"]
        + base_carbon_intensity["Petroleum"] * row["Petroleum_per"]
        + base_carbon_intensity["Solar"] * row["Solar_per"]
        + base_carbon_intensity["Wind"] * row["Wind_per"] )/100
    return result



def calculate_carbon_intensity(row, methodType):
    '''
    '''
    methods = {
        "codecarbon1":method_codecarbon1
    }
    return methods[methodType](row)
    


# Function to apply to the DataFrame
# def calculate_and_add_column(df, input1, input2):
#     # Apply the function to each row of the DataFrame
#     df['New_Column'] = df.apply(lambda row: calculate_carbon_intensity(row, input1, input2), axis=1)
#     return df

# Call the function to calculate and add the new column
# df = calculate_and_add_column(df, input1, input2)

# Display the updated DataFrame
# print(df)
