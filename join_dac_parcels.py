#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 22:44:21 2024

@author: jeostro
"""
# Script 5
## Purpose: spatial join of DAC and parcel data

# Import modules 

import pandas as pd
import numpy as np
import requests
import geopandas as gpd
import matplotlib.pyplot as plt
import fiona
import seaborn as sns

# Read in files

parcels = gpd.read_file("parcels.gpkg")

dac = gpd.read_file("dac_designation_sm.gpkg")

# Check dataframes

print(parcels.info())   

print(dac.info()) 

# Rename columns

parcels = parcels.rename(columns={"COUNTY_NAM":"COUNTY_NAME"})

dac = dac.rename(columns={"Household_Count":"household_count"})

# Set DAC CRS to parcels CRS

dac = dac.to_crs(parcels.crs)

# Do spatial join of DAC's and appropriate parcels: find approp parcels inside DACs

spat_join = parcels.sjoin(dac,how="left",predicate="within")
print(spat_join.info())

# Save the parcels that are within DACs

dac_parcels = spat_join.dropna(subset="tract")
print(dac_parcels)

# Set pop_total column type to integer

dac_parcels["pop_total"] = dac_parcels["pop_total"].astype(int)

# Save layer of parcels in DACs

dac_parcels.to_file("joined_dac_parcels.gpkg",layer="joined")

#%%
# Find total number of approp parcels in DACs

print("\nNumber of DAC parcels:",len(spat_join))

# Calculate total calc_acres of parcels within DACs

print("\nTotal acres:",spat_join["CALC_ACRES"].sum())

# Find sum of appropriate acres by municipality

acres_muni = spat_join.groupby("MUNI_NAME")["CALC_ACRES"].sum().sort_values(ascending=False)
print("\nAcres by municipality:",acres_muni.head(20))

# Find sum of appropriate acres within each county

spat_join_acres_co = spat_join.groupby("COUNTY_NAME")["CALC_ACRES"].sum().sort_values(ascending=False)
print("\nAcres by county:",spat_join_acres_co)

# Group by tract and sum acres

by_tract_acres = spat_join.groupby("tract")["CALC_ACRES"].sum().sort_values(ascending=False)
print("\nAcres by tract:",by_tract_acres)

# Group by tract and sum household counts

by_tract_hh = spat_join.groupby("tract")["household_count"].sum().sort_values(ascending=False)
print("\nHouseholds by tract:",by_tract_hh)

#%%
# Create lists of upstate and downstate counties, so can later graph acres by state area

# Create list of upstate counties

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

# Create list of downstate counties

downstate = [
    "Putnam", "Westchester", "Nassau", "Suffolk", "Bronx", "Queens", "New York",
    "Kings", "Richmond"
    ]

# Loop over column to assign by county to upstate or downstate in new column

dac_parcels["region"] = None

for index, c in dac_parcels.iterrows():
    if c["COUNTY_NAME"] in upstate:
        dac_parcels.at[index,"region"] = "upstate"
    else:
        dac_parcels.at[index,"region"] = "downstate"
        
# Check dataframe

print(dac_parcels)

# Improve figure resolution

plt.rcParams["figure.dpi"] = 300

##THESE BAR PROPORTIONS LOOK WRONG, BUT CAN DO PIE CHART INSTEAD; Create plot for acres by part of state 

fg = sns.barplot(data=dac_parcels,x="region",y="CALC_ACRES")

# Check acres sums

dac_upstate = dac_parcels.query("region=='upstate'")
print(dac_upstate["CALC_ACRES"].sum())  
dac_downstate = dac_parcels.query("region=='downstate'")
print(dac_downstate["CALC_ACRES"].sum())  

# Create pie chart for acres by region of state

fig = plt.figure(figsize=(10, 7))
labels = "Downstate", "Upstate"
fig.suptitle("Acres by Region")
colors = sns.color_palette("colorblind")
#part = dac_parcels["region"] 
data = dac_parcels.groupby("region")["CALC_ACRES"].sum()
data = round(data)
print(data)
data.plot.pie(labels=labels,colors=colors)
fig.tight_layout()

#fig.savefig(.png)

# Create pie chart for population by region of state

fig = plt.figure(figsize=(10, 7))
labels = "Downstate", "Upstate"
fig.suptitle("Population by Region")
colors = sns.color_palette("bright")
data1 = dac_parcels.groupby("region")["pop_total"].sum()
print(data1)
data1.plot.pie(labels=labels,colors=colors)
fig.tight_layout()
#fig.savefig(.png)

#%%
### DELETE THIS PROB; Make some charts

# Improve figure resolution

plt.rcParams["figure.dpi"] = 300

# Create bar plot of counties and acres

fg = sns.barplot(data=spat_join,x="COUNTY_NAME",y="CALC_ACRES")

#%%
## DIDNT WORK?? Construct graph of acres and counties
                 
# Set axis labels

fig.set_axis_labels("County","Parcel Acres in DAC")

# Tighten figure layout

fig.tight_layout()

# Save figure

fig.savefig("Acres_by_County.png")