#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 17:10:39 2024

@author: jeostro

Script 6/6
Purpose: This dissolves the DAC tract boundaries, creates a 15-mile buffer 
    around them, and locates parcels within the DACs and within the 
    buffer using spatial joins. The goal is to make a list of parcels that are 
    outside of DACs but within the 15-mile buffer. This also creates geopackage
    layers.

Required input files:
    -"dac_designation.gpkg"
    -"spat_join.gpkg"

"""

# Import modules

import pandas as pd
import geopandas as gpd

# Read in DAC shapefile and parcels file

tracts = gpd.read_file("dac_designation.gpkg")

parcels = gpd.read_file("spat_join.gpkg")

# Dissolve DAC census tracts from shapefile

dissolved = tracts.dissolve()

# Set dissolved CRS to parcels CRS

dissolved = dissolved.to_crs(parcels.crs)

# Reset index and print

dissolved = dissolved.reset_index()
print(dissolved)

# Save dissolved DAC tracts to geopackage as layer

dissolved.to_file("dissolved.gpkg",layer="tracts_dac")

#%%
## Build buffer around DAC tracts

# Set radius of buffer to 15 miles, coverted to meters

radius_m = 15*1609.34

# Create buffer layer and reset index

buffer = dissolved.buffer(radius_m)
buffer = buffer.reset_index()

# Save buffer to same geopackage file as layer

buffer.to_file("dissolved.gpkg",layer="buffer")

#%%

# Do spatial join (inner) to find parcels within buffer

parcels_buffer = parcels.sjoin(buffer)

# Save parcels within buffer only (where parcels are not within DACs),
# reset index, print

parcels_buffer = parcels_buffer[parcels_buffer["Tract"].isna()]
parcels_buffer = parcels_buffer.reset_index()
print(parcels_buffer)

# Drop extra columns

parcels_buffer = parcels_buffer.drop(columns=[
    "index_right","index","level_0","CITYTOWN_S","PROP_CLASS","ACRES", "Tract",
    "Total_Population","Households"
    ])

# Save to file

parcels_buffer.to_file("dissolved.gpkg",layer="parcels_within_buffer")

# Save to csv

parcels_buffer.to_csv("parcels_within_buffer.csv")