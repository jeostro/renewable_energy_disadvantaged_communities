#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 17:10:39 2024

@author: jeostro

Script 6/6
Purpose: This dissolves the DAC tract boundaries, creates a 15-mile buffer 
    around them, and locates parcels within & outside the DACs and within the 
    buffer using spatial joins. The goal is to make a list of parcels that are 
    outside of DACs but within the 15-mile buffer. This also creates geopackage
    layers.

Required input files:
    -"dac_designation.gpkg"
    -"parcels.gpkg"

"""

# Import modules

import pandas as pd
import numpy as np
import requests
import geopandas as gpd
import matplotlib.pyplot as plt
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

parcels_buffer = parcels.sjoin(buffer,how="left")
print(parcels_buffer)

# Drop extra columns

parcels_buffer = parcels_buffer.drop(columns=[
    "index_right","index","CITYTOWN_S","PROP_CLASS","ACRES"
    ])

# Save to file as layer

parcels_buffer.to_file("dissolved.gpkg",layer="parcels_buffer")

# Keep parcels that are within buffer

#parcels_buffer = parcels_buffer[parcels_buffer[["geometry"]!="nan"]

# DON'T NEED TO DO THIS?? Drop missing radius data
# parcels_buffer_keep = parcels_buffer.dropna(subset="radius_m")

# Set dissolved CRS to DAC tracts CRS

parcels_buffer = parcels_buffer.to_crs(tracts.crs)

# Drop extra columns in "tracts" and print

tracts = tracts.drop(columns=[
    "STATEFP","COUNTYFP","TRACTCE","AFFGEOID","LSAD","ALAND","AWATER","REDC",
    "County Name","City_Town","NYC_Region","Urban_Rural",
    "Household_Low_Count_Flag","Population_Count","Household_Count",
    "Percentile_Rank_Combined_Statewide","Percentile_Rank_Combined_NYC",
    "Percentile_Rank_Combined_ROS","Combined_Score","Burden_Score_Percentile",
    "Vulnerability_Score_Percentile","Burden_Score","Vulnerability_Score",
    "Benzene_Concentration","Particulate_Matter_25","Traffic_Truck_Highways",
    "Traffic_Number_Vehicles","Wastewater_Discharge","Housing_Vacancy_Rate",
    "Industrial_Land_Use","Landfills","Oil_Storage","Municipal_Waste_Combustors",
    "Power_Generation_Facilities","RMP_Sites","Remediation_Sites",
    "Scrap_Metal_Processing","Agricultural_Land_Use","Coastal_Flooding_Storm_Risk",
    "Days_Above_90_Degrees_2050","Drive_Time_Healthcare","Inland_Flooding_Risk",
    "Low_Vegetative_Cover","Asian_Percent","Black_African_American_Percent",
    "Redlining_Updated","Latino_Percent","English_Proficiency","Native_Indigenous",
    "LMI_80_AMI","LMI_Poverty_Federal","Population_No_College",
    "Household_Single_Parent","Unemployment_Rate","Asthma_ED_Rate","COPD_ED_Rate",
    "Households_Disabled","Low_Birth_Weight","MI_Hospitalization_Rate",
    "Health_Insurance_Rate","Age_Over_65","Premature_Deaths","Internet_Access",
    "Home_Energy_Affordability","Homes_Built_Before_1960","Mobile_Homes",
    "Rent_Percent_Income","Renter_Percent","pop_total"
    ])
print(tracts)

# NEED HOW=LEFT HERE? Do spatial join to find parcels within DAC tracts

parcels_dac = parcels_buffer.sjoin(tracts,how="left")
print(parcels_dac)

# Drop columns

parcels_dac = parcels_dac.drop(columns=["state","county"])

# Drop where "tract" is missing

parcels_dac = parcels_dac.dropna(subset="tract")

# Reset index

parcels_dac = parcels_dac.reset_index()
               
# Save parcels within DACs as layer

parcels_dac.to_file("dissolved.gpkg",layer="dac_parcels")

## STILL NEED TO GET THESE: Save dataframe of parcels in buffer but not in DACs
#check = parcels_dac["geometry"] != parcels_buffer["geometry"]

#%%

