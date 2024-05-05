#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 23:15:33 2024

@author: jeostro
"""
##THIS FILE PROB NOT NECESSARY ANYMORE, bc Wilcoxen gave me a trimmed file of NY centroids with certain cols to use
## Purpose: Read NYS parcel data (entire), save as gpkg

# Import modules; import fiona to help read parcel Centroids

import pandas as pd
import numpy as np
import requests
import geopandas as gpd
import matplotlib.pyplot as plt
import fiona

# Create layer of Centroid points from NYS tax parcel data

layer = fiona.listlayers("NYS-Tax-Parcel-Centroid-Points.gdb.zip")

# Read NYS tax parcel data ##NOT YET FINISHED (THIS TAKES V LONG ON MY COMP!)

parcels = gpd.read_file("NYS-Tax-Parcel-Centroid-Points.gdb.zip",layer="NYS_Tax_Parcels_Centroid_Points") 
print(parcels.info())

##NOTE, prof gave me 1% & 0.2% samples with about 50k & 10k centroids to practice w, bc files were big/slow on my comp.
    #no Python code here
#%%
# Save layer to geopackage file??

parcels.to_file("centroids.gpkg",layer="")



# Create sample of data and save it, to save time while practicing

sample = parcels.sample(frac=0.01)
sample.to_file("sample.gpkg")