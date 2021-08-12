import re
import pandas as pd
import sqlite3 as sql
import matplotlib.pyplot as plt
import numpy as np
from config import *

# Define helper functions
def Merge(dict1, dict2):
    return(dict2.update(dict1))

# Load up the individual Datasets
violence = pd.read_csv("data/stage3.csv")
cities = pd.read_csv("data/us cities/uscities.csv")
population = pd.read_csv("data/co-est2019-alldata.csv")
poverty_2016 = pd.read_excel('data/est16all.xls', skiprows=[0, 1, 2])
poverty_2017 = pd.read_excel('data/est17all.xls', skiprows=[0, 1, 2])
poverty_2018 = pd.read_excel('data/est18all.xls', skiprows=[0, 1, 2])
poverty_2019 = pd.read_excel('data/est19all.xls', skiprows=[0, 1, 2])


# NOTES: Fips format is SSCCC. States have a CCC of 000. The United States has a fips code of 00000.


# Select the specific columns for each DataFrame
raw_cities = cities[['city', 'state_id', 'state_name', 'county_fips', 'county_name', 'lat', 'lng', 'density', 'military', 'ranking', 'zips']]

# Splits the State and County fips codes into separate columns
select_cities = raw_cities.copy()
select_cities['state_fips'] = select_cities['county_fips'].apply(lambda x: int(str('{0:0>5}'.format(x))[:-3]))
select_cities['county_fips'] = select_cities['county_fips'].apply(lambda x: int(str('{0:0>5}'.format(x))[-3:]))
cities_dict = {'state_name':'state', 'county_name':'county'}



#                     # fips   # fips    name      name
population_columns = ['STATE', 'COUNTY', #'STNAME', 'CTYNAME',
                                'POPESTIMATE2016', 'POPESTIMATE2017', 'POPESTIMATE2018', 'POPESTIMATE2019',
                                'NPOPCHG_2016', 'NPOPCHG_2017', 'NPOPCHG_2018', 'NPOPCHG_2019',
                                'BIRTHS2016', 'BIRTHS2017', 'BIRTHS2018', 'BIRTHS2019',
                                'DEATHS2016', 'DEATHS2017', 'DEATHS2018', 'DEATHS2019',
                                'INTERNATIONALMIG2016', 'INTERNATIONALMIG2017', 'INTERNATIONALMIG2018', 'INTERNATIONALMIG2019',
                                'DOMESTICMIG2016', 'DOMESTICMIG2017', 'DOMESTICMIG2018', 'DOMESTICMIG2019',
                                'NETMIG2016', 'NETMIG2017', 'NETMIG2018', 'NETMIG2019',
                                'GQESTIMATES2016', 'GQESTIMATES2017', 'GQESTIMATES2018', 'GQESTIMATES2019',
                                'RBIRTH2016', 'RBIRTH2017', 'RBIRTH2018', 'RBIRTH2019',
                                'RDEATH2016', 'RDEATH2017', 'RDEATH2018', 'RDEATH2019',
                                'RINTERNATIONALMIG2016', 'RINTERNATIONALMIG2017', 'RINTERNATIONALMIG2018', 'RINTERNATIONALMIG2019',
                                'RDOMESTICMIG2016', 'RDOMESTICMIG2017', 'RDOMESTICMIG2018', 'RDOMESTICMIG2019',
                                'RNETMIG2016', 'RNETMIG2017', 'RNETMIG2018', 'RNETMIG2019']
population_dict = {'STATE':'state_fips', 'COUNTY':'county_fips', 'STNAME':'state', 'CTYNAME':'county'}

#                                   # fips             # fips              2 postal       continent/state/county
poverty_dict_1 = {'State FIPS Code': 'state_fips', 'County FIPS Code': 'county_fips'}

poverty_dict_2016 = {'State FIPS Code': 'state_fips', 'County FIPS Code': 'county_fips',
                     'Poverty Estimate, All Ages': 'Poverty_Est_All_2016', 'Poverty Percent, All Ages': 'Poverty_Perc_All_2016',
                     'Poverty Estimate, Age 0-17': 'Poverty_Est_0_17_2016', 'Poverty Percent, Age 0-17': 'Poverty_Perc_0_17_2016',
                     'Poverty Estimate, Age 5-17 in Families': 'Poverty_Est_Families_5_17_2016',
                     'Poverty Percent, Age 5-17 in Families': 'Poverty_Perc_Families_5_17_2016',
                     'Median Household Income':'Median_Household_Income_2016'}

poverty_dict_2017 = {'State FIPS Code': 'state_fips', 'County FIPS Code': 'county_fips',
                     'Poverty Estimate, All Ages': 'Poverty_Est_All_2017', 'Poverty Percent, All Ages': 'Poverty_Perc_All_2017',
                     'Poverty Estimate, Age 0-17': 'Poverty_Est_0_17_2017', 'Poverty Percent, Age 0-17': 'Poverty_Perc_0_17_2017',
                     'Poverty Estimate, Age 5-17 in Families': 'Poverty_Est_Families_5_17_2017',
                     'Poverty Percent, Age 5-17 in Families': 'Poverty_Perc_Families_5_17_2017',
                     'Median Household Income': 'Median_Household_Income_2017'}

poverty_dict_2018 = {'State FIPS Code': 'state_fips', 'County FIPS Code': 'county_fips',
                     'Poverty Estimate, All Ages': 'Poverty_Est_All_2018', 'Poverty Percent, All Ages': 'Poverty_Perc_All_2018',
                     'Poverty Estimate, Age 0-17': 'Poverty_Est_0_17_2018', 'Poverty Percent, Age 0-17': 'Poverty_Perc_0_17_2018',
                     'Poverty Estimate, Age 5-17 in Families': 'Poverty_Est_Families_5_17_2018',
                     'Poverty Percent, Age 5-17 in Families': 'Poverty_Perc_Families_5_17_2018',
                     'Median Household Income': 'Median_Household_Income_2018'}

poverty_dict_2019 = {'State FIPS Code': 'state_fips', 'County FIPS Code': 'county_fips',
                     'Poverty Estimate, All Ages': 'Poverty_Est_All_2019', 'Poverty Percent, All Ages': 'Poverty_Perc_All_2019',
                     'Poverty Estimate, Age 0-17': 'Poverty_Est_0_17_2019', 'Poverty Percent, Age 0-17': 'Poverty_Perc_0_17_2019',
                     'Poverty Estimate, Age 5-17 in Families': 'Poverty_Est_Families_5_17_2019',
                     'Poverty Percent, Age 5-17 in Families': 'Poverty_Perc_Families_5_17_2019',
                     'Median Household Income': 'Median_Household_Income_2019'}

poverty_columns = ['State FIPS Code', 'County FIPS Code',
                                    'Poverty Estimate, All Ages', 'Poverty Percent, All Ages',
                                    'Poverty Estimate, Age 0-17', 'Poverty Percent, Age 0-17',
                                    'Poverty Estimate, Age 5-17 in Families', 'Poverty Percent, Age 5-17 in Families',
                                    'Median Household Income']

# Rename columns as appropriate using Dictionaries and select the appropriate columns.
select_cities       = select_cities.rename(columns=cities_dict)
select_poverty_2016 = poverty_2016[poverty_columns].rename(columns=poverty_dict_2016)
select_poverty_2017 = poverty_2017[poverty_columns].rename(columns=poverty_dict_2017)
select_poverty_2018 = poverty_2018[poverty_columns].rename(columns=poverty_dict_2018)
select_poverty_2019 = poverty_2019[poverty_columns].rename(columns=poverty_dict_2019)
select_population   = population[population_columns].rename(columns=population_dict)

# Removes the County suffix from the county column data.
#select_population['county'] = select_population['county'].apply(lambda x: x[:-7] if(' County' in x) else x)

# Populates the counties column using the counties provided in the city_or_county columns.
violence['v_county'] = violence['city_or_county'].apply(lambda x: x[:-9] if(' (county)' in x) else pd.NA)

# Correct the city column by removing the counties.
violence['city'] = violence['city_or_county'].apply(lambda x: pd.NA if(' (county)' in x) else x)
violence = violence.drop(columns='city_or_county')

# Merge the datasets together on the appropriate columns.
d1 = violence.merge(select_cities, on=['state', 'city'], how='left', sort=False)
d2 = d1.merge(select_population, on=['state_fips', 'county_fips'], how='inner', sort=False)
d3 = d2.merge(select_poverty_2016, on=['state_fips', 'county_fips'], how='inner', sort=False)
d4 = d3.merge(select_poverty_2017, on=['state_fips', 'county_fips'], how='inner', sort=False)
d5 = d4.merge(select_poverty_2018, on=['state_fips', 'county_fips'], how='inner', sort=False)
d6 = d5.merge(select_poverty_2019, on=['state_fips', 'county_fips'], how='inner', sort=False)
d6.to_csv('data/joint_dataset2.csv')




"""
cities_population_joint = select_cities.merge(select_population, on=['state_fips', 'county_fips', 'state', 'county'], how='inner', sort=False)
city_pop_pov16_joint = cities_population_joint.merge(select_poverty_2016, on=['state_fips', 'county_fips'], how='inner', sort=False)
city_pop_pov17_joint = city_pop_pov16_joint.merge(select_poverty_2017, on=['state_fips', 'county_fips'], how='inner', sort=False)
city_pop_pov18_joint = city_pop_pov17_joint.merge(select_poverty_2018, on=['state_fips', 'county_fips'], how='inner', sort=False)
city_pop_pov19_joint = city_pop_pov18_joint.merge(select_poverty_2019, on=['state_fips', 'county_fips'], how='inner', sort=False)

# Merge the original way
#full_dataset         = violence.merge(city_pop_pov19_joint, on=['state', 'city'], how='left', sort=False)
#full_dataset         = full_dataset.dropna(subset=['incident_id', 'county_fips', 'state_fips', 'county'], how='any')
#full_dataset.to_csv('data/joint_dataset.csv')

# Merge the other way
full_dataset         = violence.merge(city_pop_pov19_joint, on=['state', 'city'], how='left', sort=False)
#full_dataset         = full_dataset.dropna(subset=['incident_id'], how='any')
#full_dataset         = full_dataset.dropnull(subset=['incident_id'], how='any')
print(full_dataset.shape)
#full_dataset         = city_pop_pov19_joint.merge(violence, on=['state', 'city'], how='right', sort=False)
full_dataset.to_csv('data/joint_dataset2.csv')

"""
