#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 22:58:01 2024

@author: jeostro

Script 2/6
Purpose: Trim NY tax parcels to vacant parcels & misc. agricultural parcels 
    that are 10 acres or more. Create geopackage.

Required input files:
    -“nys-tax-parcel-centroid-trim.zip", a trimmed NY tax parcel file, 
    provided by Dr. Wilcoxen.
    
"""
    
# Import modules

import pandas as pd
import geopandas as gpd

# Read file of NY centroids in geopandas 

parcels = gpd.read_file("nys-tax-parcel-centroid-trim.zip")

# Check sample columns

print(parcels.info())
 
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

# Using "CALC_ACRES" column, select parcels of 10+ acres and print

trimmed = trimmed[trimmed["CALC_ACRES"]>=10]
print (trimmed)

# Sort based on "CALC_ACRES" and print
    
trimmed = trimmed.sort_values("CALC_ACRES",ascending=False)
print(trimmed)
   
# Plot centroids

trimmed.plot(legend=True,figsize=(10, 6))

# Write to geopackage

trimmed.to_file("parcels.gpkg",layer="parcels")
