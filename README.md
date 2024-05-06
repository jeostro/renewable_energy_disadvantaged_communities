# Community Solar and Disadvantaged Communities in NY
Key question: Is there appropriate land near disadvantaged communities in NY that may be used for community solar?

## Summary
This analysis investigates the potential for solar energy production and benefits for designated disadvantaged communities (DACs) through the use of community solar in New York. The study located and mapped vacant land parcels and DACs, finding areas of overlap. It identified parcels that were within DACs and parcels located near DACs, for potential use for community solar. At a policy level, the state government provides incentives and financing options for solar projects through programs such as NY-Sun. This may encourage investment in community solar, particularly for DACs, which may have limited financial resources.

## Background
In 2019, the New York State government passed the Climate Leadership and Community Protection Act (CLCPA). The CLCPA requires statewide renewable energy development. It also recognizes that certain communities – designated as “disadvantaged communities” (DACs) – face disproportionate burdens and risks from pollution, historical disinvestment or discrimination, and climate change. The state must “invest or direct resources to ensure that disadvantaged communities receive at least 35 percent, with the goal of 40 percent, of overall benefits of spending on clean energy and energy efficiency programs” ([NYS DEC](https://dec.ny.gov/news/press-releases/2023/3/new-york-state-climate-justice-working-group-finalizes-disadvantaged-communities-criteria-to-advance-climate-justice#:~:text=The%20Climate%20Act%20requires%20New,Climate%20Act%20prioritizes%20climate%20justice.)). In 2023, a working group finalized criteria for DACs, and it published identified DACs in the state.

Community solar is a solar project or purchasing program, within a geographic area, that provides benefits to multiple customers (source: The US Department of Energy). In most cases, customers subscribe to a project and benefit from energy generated by solar panels at an off-site array. People receive monthly credits on their electricity bills for the electricity produced by these solar panels([The Washington Post](https://www.washingtonpost.com/climate-environment/2023/10/10/community-solar-renters-apartments-discounted-electricity/)). Community solar allows people who cannot install their own solar panels and those who do not own their homes to benefit from clean energy. The typical solar array requires at least 10 acres of land in NY ([NYSDERA](https://www.nyserda.ny.gov/All-Programs/NY-Sun/Solar-for-Your-Business/How-to-Go-Solar/Leasing-Your-Land)), and households should be located within about 15 miles of an array to decarbonize the local utility grid ([The Washington Post](https://www.washingtonpost.com/climate-environment/2023/10/10/community-solar-renters-apartments-discounted-electricity/)).

By analyzing vacant land parcels and DACs in NY, this project attempts to locate parcels that could be used to install community solar arrays that benefit DACs.

## Input Data
Final Disadvantaged Communities (DAC) 2023 CSV, downloaded from Open Data NY: https://data.ny.gov/Energy-Environment/Final-Disadvantaged-Communities-DAC-2023/2e6c-s6fp/about_data

Cartographic boundary shapefile for 2019 NY Census tracts, downloaded from US Census Bureau: https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html (Click “2019,” scroll to “Census Tracts,” and within the “500,000 (state) shapefile” dropdown menu, select “New York.”)

Cartographic boundary shapefile for counties, downloaded from US Census Bureau: https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html 
(On the “2023” tab, scroll to “Counties” and download the “5,000,000 (national) shapefile.”)

US Census Bureau 2010 data: The study used a US Census Data API Key to retrieve/download relevant data. This was done in the dacs_check.py script. Census API keys are available here: https://api.census.gov/data/key_signup.html

NYS Tax Parcel Centroid Points, available at NYS GIS Clearinghouse: https://data.gis.ny.gov/datasets/5fe2f8c9507a434487e1db85c905d1b3_0/explore?location=42.643566%2C-75.816900%2C6.88
(Note: Because the original file is so large, I used a smaller file provided by Dr. Wilcoxen that omits some unnecessary columns. It is named “nys-tax-parcel-centroid-trim.zip.” The “ny_centroids.py” script below uses this file instead of a direct download from NYS GIS Clearinghouse. The trimmed file is quite large as well, so it is not saved in the project repository.)

## Scripts

### dac_check.py
Run this script first. This investigates which version of Census data the state used to define DACs. This script reads a 2019 Census shapefile and verifies that the state uses the 2010 Census tracts in NY to define DACs. It retrieves 2010 Census data using an API and merges the DAC and Census data, as a check on the original DAC file. This script also creates a geopackage layer of DACs.

### ny_centroids.py
Run this script second. It filters NY parcel data parcels to those that are classified as vacant land, miscellaneous agricultural land, and 10 or more acres in size. This also creates a geopackage layer of the filtered parcels.

### dac_smaller.py
Run this script third. This filters the DAC data to only a few columns, so the size is more manageable for later merges. This also creates a geopackage.

### ny_county_boundaries.py
Run this script fourth. This creates a geopackage layer of NY counties using a US Census Bureau cartographic boundary shapefile.

### join_dac_parcels.py
Run this script fifth. This runs a spatial join of the “dac_smaller” data and the parcel data and creates a geopackage. It then analyzes parcels and acres by grouping data, performing summary statistics, and creating pie charts. It does an analysis of data based on Upstate and Downstate regions.

### dissolved.py
Run this script last. This dissolves the DAC tract boundaries, creates a 15-mile buffer around them, and locates parcels within the DACs and the buffer using spatial joins. This also creates geopackage layers.

Note: Open QGIS and use the DAC layer, parcel layer, county boundary layer, and dissolved layers to create a map. 

## Additional Files
The repository contains an additional file that explains final DAC criteria: “Disadvantaged Communities Criteria Fact Sheet [PDF]” from https://climate.ny.gov/Resources/Disadvantaged-Communities-Criteria

## Analysis and Results


[I'm a test link](https://www.google.com)
