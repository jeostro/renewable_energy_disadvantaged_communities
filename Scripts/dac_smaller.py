#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 18:27:22 2024

@author: jeostro

Script 3/6
Purpose: Filter DAC data to only a few columns, so the size is more manageable 
    for later merges. Create geopackage.
    
Required input files:
    -"dac_designation.gpkg"

"""
    
# Import modules

import pandas as pd
import geopandas as gpd

# Read joined DAC data

dac_sm = gpd.read_file("dac_designation.gpkg")

# Save only a few columns to make file smaller

dac_sm = dac_sm[["tract","geometry","pop_total","Household_Count"]]

# Check dataframe

print(dac_sm)

# Save "dac_sm" as geopackage

dac_sm.to_file("dac_designation_sm.gpkg",layer="dac_sm")
