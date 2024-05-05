#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 21:04:18 2024

@author: jeostro

Script 1/6
Purpose: Determine whether DAC data uses 2010 or 2020 Census data. 
    Merge DAC and Census data and check for tract alignment. Create geopackage.

Required input files:
    -"Final_Disadvantaged_Communities__DAC__2023_20240502.csv", downloaded from 
    Open Data NY: https://data.ny.gov/Energy-Environment/Final-Disadvantaged-Communities-DAC-2023/2e6c-s6fp/about_data
    -"cb_2019_36_tract_500k.zip", downloaded from US Census Bureau: 
    https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html 
    -Census API key, which can be acquired here: https://api.census.gov/data/key_signup.html

"""

# Import modules 

import pandas as pd
import numpy as np
import requests
import geopandas as gpd
import fiona

# Import DACs CSV

dac = pd.read_csv("Final_Disadvantaged_Communities__DAC__2023_20240502.csv", dtype=str)

# Drop extra geometry column

dac = dac.drop(columns="the_geom")

# Delete unnamed

unnamed = [c for c in dac.columns if c.startswith("Unname")]
dac = dac.drop(columns=unnamed)

# Keep only DAC-designated areas in the df, to assist with processing speed

dac = dac[dac["DAC_Designation"]=="Designated as DAC"]

# Check DAC dataframe

print(dac)

# View DAC columns

print(dac.info())         

# Read Census 2019 tract shapefile

census = gpd.read_file("cb_2019_36_tract_500k.zip") 

# Check columns

print(census.info())

# Merge Census data with DAC data 

census = census.merge(dac,on="GEOID",how="left",indicator=True)

# Check merge indicator and drop it

print(census["_merge"].value_counts())
census = census.drop(columns="_merge")

#%%
## Retrieve 2019 Census info using API

variables = {"B01001_001E":"pop_total"}

# Create variable and use keys method to obtain list of keys

var_list = variables.keys()

# Use join method to join elements with commas

var_string = ",".join(var_list)

# Set API endpoint

api = "https://api.census.gov/data/2019/acs/acs5"

## Set up payload and call the Census API

# Set "for" clause for Census query to retrieve tract data

for_clause = 'tract:*'

# Set "in" clause for Census query to retrieve all NYS county data

in_clause = 'state:36 county:*'

# Set key value to Census API key

key_value = "7a1ea56940cb0710832f37792711f217bb41d0c4"

# Create dictionary 

payload = {'get':var_string, 'for':for_clause, 'in':in_clause, 'key':key_value}

# Build query string, send it to API endpoint, collect response

response = requests.get(api,payload)

# Test response status code

if response.status_code != 200:
    print(response.status_code)
    print(response.text)
    assert False
    
# Parse JSON returned by Census server

row_list = response.json()

# Select a row

colnames = row_list[0]

# Select remaining rows with other variable

datarows = row_list[1:]

# Convert data into Pandas dataframe "pop"

pop = pd.DataFrame(columns=colnames,data=datarows)

# Check "pop"

print(pop)

#%%
# Clean missing data

pop = pop.replace("-666666666",np.nan)

# Rename columns of pop using earlier dictionary and print

pop = pop.rename(columns=variables)

print(pop)

# Create new GEOID column

pop["GEOID"] = pop["state"]+pop["county"]+pop["tract"]

# Set index of pop

pop = pop.set_index("GEOID")

# Check dataframes

print("\nCensus:",census)
print("\npop:",pop)

#%%
# Join pop onto Census data and print

join = census.merge(pop,how="outer",on="GEOID",indicator=True)
print("\nJoin:",join)

# Check merge indicator's value counts to verify all records matched

print(join["_merge"].value_counts())

# Check number of records

print(len(join))

# Remove right-only values with no geometry

join = join[join["_merge"]!="right_only"]

# Print dataframe and number of records to verify drop

print(join)
print(len(join))

# Drop merge indicator column

join = join.drop(columns="_merge")

# Keep only DAC-designated areas in the df, to assist with processing speed

join = join[join["DAC_Designation"]=="Designated as DAC"]
print(join)

# To resolve problem from a merge, rename column name to match similar column

join = join.rename(columns={"County": "County Name"})
print(join)

# Save "join" as geopackage

join.to_file("dac_designation.gpkg",layer="dac")

