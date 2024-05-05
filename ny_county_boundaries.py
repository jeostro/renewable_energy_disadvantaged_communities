#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 20:45:26 2024

@author: jeostro

Script 4/6
Purpose: Create a geopackage layer of NY counties.

Required input files:
    -"cb_2023_us_county_5m.zip", downloaded from US Census Bureau:
    https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html
    
"""

# Import modules

import pandas as pd
import geopandas as gpd

# Read in file

counties = gpd.read_file("cb_2023_us_county_5m.zip") 

# Check columns

print(counties.info())

# Select only NYS counties

counties = counties.query("STATEFP=='36'")

# Check columns

print(counties)

# Write to file

counties.to_file("all_counties.gpkg",layer="counties")
