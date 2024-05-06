#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 22:44:21 2024

@author: jeostro

Script 5/6
Purpose: Do a spatial join of the “dac_smaller” data and the parcel data, and 
    create geopackage. Analyze parcels and acres by grouping data, performing 
    summary statistics, and creating charts. Analyze data by Upstate and 
    Downstate regions.
    
Required input files:
    -"parcels.gpkg"
    -"dac_designation_sm.gpkg"

"""

# Import modules 

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

# Read in files

parcels = gpd.read_file("parcels.gpkg")

dac = gpd.read_file("dac_designation_sm.gpkg")

# Check dataframes

print(parcels.info())   

print(dac.info()) 

# Rename columns

parcels = parcels.rename(columns={"COUNTY_NAM":"COUNTY_NAME","CALC_ACRES":"Calculated_Acres"})

dac = dac.rename(columns={"tract":"Tract","Household_Count":"Households","pop_total":"Total_Population"})

# Set DAC CRS to parcels CRS

dac = dac.to_crs(parcels.crs)

# Do spatial join to find parcels inside DACs and reset index

spat_join = parcels.sjoin(dac,how="left",predicate="within")
spat_join = spat_join.reset_index()

# Drop columns and print

spat_join = spat_join.drop(columns={"index","index_right"})
print(spat_join)

# Save file 

spat_join.to_file("spat_join.gpkg")

#%%
# Save the parcels that are within DACs, reset index, drop column, print

dac_parcels = spat_join.dropna(subset="Tract")
dac_parcels = dac_parcels.reset_index()
dac_parcels = dac_parcels.drop(columns="index")
print(dac_parcels)

# Set population and household column types to integer and print

dac_parcels[["Total_Population","Households"]] = dac_parcels[["Total_Population","Households"]].astype(int)
print(dac_parcels)

# Save parcels in DACs as layer, for later map

dac_parcels.to_file("joined_dac_parcels.gpkg",layer="dac_parcels")

#%%
# Find total number of good parcels in DACs

print("\nNumber of DAC parcels:",len(dac_parcels))

# Calculate total acres of parcels within DACs

print("\nTotal acres:",dac_parcels["Calculated_Acres"].sum())

# Find sum of good acres by municipality

acres_muni = dac_parcels.groupby("MUNI_NAME")["Calculated_Acres"].sum().sort_values(ascending=False)
print("\nAcres by municipality:",acres_muni.head(20))

# Find sum of good acres within each county

acres_co = dac_parcels.groupby("COUNTY_NAME")["Calculated_Acres"].sum().sort_values(ascending=False)
print("\nAcres by county:",acres_co)

# Group by tract and sum good acres

by_tract_acres = dac_parcels.groupby("Tract")["Calculated_Acres"].sum().sort_values(ascending=False)
print("\nAcres by tract:",by_tract_acres)

# Group by tract and sum household counts

by_tract_hh = dac_parcels.groupby("Tract")["Households"].sum().sort_values(ascending=False)
print("\nHouseholds by tract:",by_tract_hh)

# TEST; Write to csv

by_tract_hh.to_csv("by_tract.csv")

#%%
# Create lists of upstate and downstate counties

upstate = [
    "Albany", "Allegany", "Broome", "Cattaraugus", "Cayuga", "Chautauqua", "Chemung",
    "Chenango", "Clinton", "Columbia", "Cortland", "Delaware", "Dutchess", "Erie",
    "Essex", "Franklin", "Fulton", "Genesee", "Greene", "Hamilton", "Herkimer", 
    "Jefferson", "Lewis", "Livingston", "Madison", "Montgomery", "Monroe",
    "Niagara", "Oneida", "Onondaga", "Ontario", "Orange", "Orleans", "Oswego", 
    "Otsego", "Rensselaer", "Rockland", "Schenectady", "Schoharie", "Schuyler",
    "Seneca", "Saratoga", "StLawrence", "Steuben", "Sullivan", "Tioga", "Tompkins",
    "Ulster", "Warren", "Washington", "Wayne", "Wyoming", "Yates"
    ]

downstate = [
    "Putnam", "Westchester", "Nassau", "Suffolk", "Bronx", "Queens", "New York",
    "Kings", "Richmond"
    ]

# Loop over column to assign by county to upstate or downstate in new column

dac_parcels["Region"] = None

for index, c in dac_parcels.iterrows():
    if c["COUNTY_NAME"] in upstate:
        dac_parcels.at[index,"Region"] = "upstate"
    else:
        dac_parcels.at[index,"Region"] = "downstate"
        
# Check dataframe

print(dac_parcels)

# Improve figure resolution

plt.rcParams["figure.dpi"] = 300

# Check acres sums

dac_upstate = dac_parcels.query("Region=='upstate'")
print(dac_upstate["Calculated_Acres"].sum())  
dac_downstate = dac_parcels.query("Region=='downstate'")
print(dac_downstate["Calculated_Acres"].sum())  

# Create pie chart for acres by region of state

fig = plt.figure(figsize=(10, 7))
labels = "Downstate", "Upstate"
fig.suptitle("Acres within Disadvantaged Communities by NY Region")
colors = sns.color_palette("colorblind")
#part = dac_parcels["region"] 
data = dac_parcels.groupby("Region")["Calculated_Acres"].sum()
data = round(data)
print(data)
data.plot.pie(labels=labels,colors=colors)
fig.tight_layout()
#fig.savefig(.png)

# Create pie chart for population by region of state

fig = plt.figure(figsize=(10, 7))
labels = "Downstate", "Upstate"
fig.suptitle("Population by NY Region")
colors = sns.color_palette("bright")
data1 = dac_parcels.groupby("Region")["Total_Population"].sum()
print(data1)
data1.plot.pie(labels=labels,colors=colors)
fig.tight_layout()
#fig.savefig(.png)