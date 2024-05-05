#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 17:10:39 2024

@author: jeostro
"""
# Script 6.  # Purpose: Dissolve DAC tract boundaries, create a 15-mile buffer around them, and find parcels within and outside the DACs and boundaries through spatial joins.
# Import modules

import pandas as pd
import numpy as np
import requests
import geopandas as gpd
import matplotlib.pyplot as plt
import fiona
import os

# Read in DAC shapefile and parcels file

tracts = gpd.read_file("dac_designation.gpkg")

parcels = gpd.read_file("parcels.gpkg")

# Dissolve DAC census tracts from shapefile

dissolved = tracts.dissolve()

# Set dissolved CRS to parcels CRS

dissolved = dissolved.to_crs(parcels.crs)

# Reset index: move the index into an ordinary column to preserve it; print

dissolved = dissolved.reset_index()

print(dissolved)

# Save dissolved DAC tracts to geopackage as layer

dissolved.to_file("dissolved.gpkg",layer="tracts_dac")

## Build buffer around DAC tracts

# Set radius of buffer to 15 miles, coverted to meters

radius_m = 15*1609.34

# Create buffer layer and reset index

buffer = dissolved.buffer(radius_m)
buffer = buffer.reset_index()

# Save buffer to same geopackage file as layer

buffer.to_file("dissolved.gpkg",layer="buffer")

## NEED HOW=LEFT HERE? Do spatial join to find parcels within buffer; print result

parcels_buffer = parcels.sjoin(buffer)
print(parcels_buffer)

# Drop extra index columns

parcels_buffer = parcels_buffer.drop(columns = ["index_right","index"])

# ?? Drop other extra columns
# parcels_buffer = parcels_buffer.drop(columns = [
  #  "state", "county", "tract", "Percentile_Rank_Combined_Statewide",
  #  "Percentile_Rank_Combined_NYC","Percentile_Rank_Combined_ROS", "Low_Vegetative_Cover"
  #  ])

# Save to file as layer

parcels_buffer.to_file("dissolved.gpkg",layer="parcels_buffer")

# Keep parcels that are within buffer

# DON'T NEED TO DO THIS?? Drop missing radius data
# parcels_buffer_keep = parcels_buffer.dropna(subset="radius_m")

# Set dissolved CRS to DAC tracts CRS

parcels_buffer = parcels_buffer.to_crs(tracts.crs)

# NEED HOW=LEFT HERE? Do spatial join to find parcels within DAC tracts

parcels_dac = parcels_buffer.sjoin(tracts)
                                 
# Reset index

parcels_dac = parcels_dac.reset_index()
               
# Save parcels within DACs as layer

parcels_dac.to_file("dissolved.gpkg",layer="dac_parcels")

## ?? Save dataframe of parcels in buffer but not in DACs
#check = parcels_dac["geometry"] != parcels_buffer["geometry"]

#%%

