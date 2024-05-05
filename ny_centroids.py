#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 22:58:01 2024

@author: jeostro
"""
# Script 2
## Purpose: Read NYS parcel data, trim to vacant & some ag parcels, trim to 10+ acres, create gpkg layer
    
# Import modules; import fiona to help read parcel centroids

import pandas as pd
import numpy as np
import requests
import geopandas as gpd
import matplotlib.pyplot as plt
import fiona

# Read file of NY centroids in geopandas 

parcels = gpd.read_file("nys-tax-parcel-centroid-trim.zip")

# Check sample columns

print(parcels.info())

# Explored parcel centroids data dictionary to identify property type classifications
 #no Python code here
 
# Select parcels with appropriate agricultural & vacant land codes
 
trimmed = parcels.query(
    "PROP_CLASS=='100' or PROP_CLASS=='300' or PROP_CLASS=='310' or PROP_CLASS=='311' or PROP_CLASS=='312' or PROP_CLASS=='314' or PROP_CLASS=='320' or PROP_CLASS=='321' or PROP_CLASS=='322' or PROP_CLASS=='330' or PROP_CLASS=='331' or PROP_CLASS=='340' or PROP_CLASS=='341' or PROP_CLASS=='350' or PROP_CLASS=='351' or PROP_CLASS=='352' or PROP_CLASS=='380'"
    )

# Check trimmed for # of parcels

print(trimmed)

## Select parcels of appropriate acreage (10+ acres)

# View parcels with the assessed acreage ("ACRES")

print(trimmed["ACRES"])

# View parcels with the GIS calculated acres ("CALC_ACRES")

print(trimmed["CALC_ACRES"])

# Using "CALC_ACRES" column (looks most exact), select parcels of 10+ acres

trimmed = trimmed[trimmed["CALC_ACRES"]>=10]
print (trimmed)

### TO DO: Get rid of very large parcels? (may be mountains)
    #Not done yet here; largest in sample is 400 acres
    
trimmed = trimmed.sort_values("CALC_ACRES",ascending=False)
print(trimmed)
   
# Plot centroids

trimmed.plot(legend=True,figsize=(10, 6))

# Write to geopackage

trimmed.to_file("parcels.gpkg",layer="parcels")
