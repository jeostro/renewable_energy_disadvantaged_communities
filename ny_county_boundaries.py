#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 20:45:26 2024

@author: jeostro
"""
# Script 4
## Purpose: Read US cartographic boundary shapefile and filter for only NYS counties, for QGIS map layer

# Import modules

import pandas as pd
import numpy as np
import requests
import geopandas as gpd
import matplotlib.pyplot as plt
import fiona

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
