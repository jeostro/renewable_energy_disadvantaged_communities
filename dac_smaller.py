#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 18:27:22 2024

@author: jeostro
"""
# Script 3
## Purpose: Pick out only needed columns of DAC before a join
    
# Import modules

import pandas as pd
import numpy as np
import requests
import geopandas as gpd

# Copy joined DAC data

dac_sm = gpd.read_file("dac_designation.gpkg")

# Save only two columns to make file smaller

dac_sm = dac_sm[["tract","geometry","pop_total","Household_Count"]]

# Check dataframe

print(dac_sm)

# Save "dac_sm" as geopackage

dac_sm.to_file("dac_designation_sm.gpkg",layer="dac_sm")
