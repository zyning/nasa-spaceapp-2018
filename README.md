# nasa-spaceapp-2018
This is the collaboration repo for nasa 2018 spaceapp challenge
“Vigil”: How Can We Use Data to Predict Domestic Fire Risk ?
Problem

Domestic fire incidents remains one of the leading causes of death that threatens human safety and increase the urban vulnerability.

To address this problem, we developed Vigil, a predictive analytics system for forecasting and prioritizing Fire Inspections in the city. The system provides insightful recommendations to help fire departments better plan both their fire fighting strategies and their awareness campaigns, and also help insurance companies to deal with damages and less importantly help indoor and outdoor fire prevention and alarm systems to better identify their customers.

(1) Building conditions (2) Demographic and economic characteristics: while the overall demographics of neighborhoods differ from one to another, most of the people inhibiting the same neighborhood share relatively similar income, similar educational level, along with other demographic characteristics as they tend to live the same life style. (3) Weather conditions: we hypothesized that the various weather features, in particular temperature and precipitation, would be a good proxy on the use of heater, AC. Other weather features like snow, wind, rain would commonly reflect some human behavioral attitudes towards staying at home.

However, cities are highly heterogeneous, and commonly unequal in regards with social behavior of their citizens, and the structure of their architectures among other dimensions. Our capacity to understand and evaluate our methods is bound by availability of contextual relevant data in different cities. To overcome the challenge of accessing to local and real data, our study test the theoretical models using the public data from the city of CA. In this project, we conducted a series of experiments to demonstrate how we collected, filtered and merged different sources of data from open data portals to develop our predictive dashboard.
Data

In this section, we describe each of the datasets that we have used. This project relies on open data sources from the City of CA. All of the data is publicly available, and pulled using the city's open data APIs. The main data sources that we used in the project are the following:

    [Fire Incident Dataset - FDNY Incidents]): The dataset contains the daily detailed information about fire incidents that are handled by FDNY Fire units. The dataset has been collected using National Fire Incident Reporting System (NFIRS) and NASA database about climate. This later is a modular all-incident reporting system designed primarily to understand the nature and causes of fire, as well as civilian fire casualties and fire-fighter injuries. The raw dataset contains 1.33M records spanned between st January 2013 and 31th Dec 2017. This dataset includes information on where and when incidents have occurred, and what resources have been used to mitigate it. The limitation we faced when we used this data source is this later doesnt provide information on the building location, but the street address.

    Census: The Census’ American Housing Survey is an annual panel conducted by the Census to track highly-specific details about households. As summarized in the literature review, there are some socio-demographic factors that relatively contribute to fire accidents.

    Street Data a digital vector file of public and private roads and streets. The dataset is maintained by the state Department of Transportation.

    Open Street Map is an open source community project dedicated to mapping the world through community contributions. In order to obtain buildings’ characteristics, we query, filter, and parse OSM API to get relevant information on buildings as well as other geographic features related to roads, buildings, Points Of Interest.

    Weather Data We obtained New York historical weather information through Weather Wunderground developer API. We collected daily weather summaries for our study period, and selected the following features: temperature, dew point, precipitation amount and type, visibility, wind, fog, pressure and humid- ity. For some features such as temperature, we obtained more granular data by taking minimum, mean and maximum values.

Analysis

In order to study and analyze spatial patterns, we started investigating the different options taking in consideration the ability to analyze distinct spatial units. US Census Bureau has designed a hierarchically nested spatial units to overcome any geographical overlap and to easily perform longitudinal analysis. In our study, the spatial granularity is defined based on the census tracts or the urban block. Census tract is a geographic unit used for census on demographic characteristics. It links geographic areas with socio-demographic dataset, to reflect the structure of homogeneous urban form regulated by current zoning ordinances. The urban block is a homogeneous physical territory bounded by streets. Census Blocks are distinct inside Census tracts, according to the 2010 Census, Manhattan is divided into 288 census tracts and 2870 urban blocks based on the PLUTO dataset. The advantage of adopting these spatial units is that both census tract, census blocks are officially used to document social and demographic statistics.

Fig.1 depicts the distribution of domestic fire accidents over time in the city of New York. We observe that there is periodic temporal pattern over the different years. The number of incidents fluctuates across the first three months of the year, indicating accidents may be in infuenced by dynamic temporal factors such as weather. There are also differences when comparing between different incidents distributions at the level of tracts. From the above observations, we decide to include data from other domains such as meteorological information to predict fire incidents.

ScreenShot Fig.1: Number of domestic fire accidents per day

In what follows, we describe the task of selecting proper feature sets to build our model. Feature engineering is the task of researching and creating features that represent the human’s understanding about the influencing factors of a phenomena. In our project, features are extracted from each individual domains, representing the influencing factors. The set of features are summarized below:
Feature Type 	Feature 	Description
Temporal 	Day of week 	The ordinal number of the day in a week
Temporal 	Month 	The month which the time interval is in
Temporal 	Holiday 	Is this day a holiday or no
Spatial 	Tract 	The administrative tract
Meteorological 	Weather condition 	The index of humidity in a given day
Meteorological 	Temperature 	The temperature in a given day
Meteorological 	Wind 	The orientation and speed of the wind in a given day
Meteorological 	Humidity 	The index of humidity in a given day
Meteorological 	Snow 	The depth of snow in a given day
Meteorological 	pressure 	The level of pressure in a given day
Meteorological 	precipitation 	The level of precipitation in a given day
Buildings 	avg_yearbuilt 	The average age of buildings in a give region
Buildings 	total_units 	Total number of units in a give region
Buildings 	avg_unitarea 	The average unit area in a give region
Buildings 	ratio_retailarea 	Ratio of retail buildings in a give region
Buildings 	ratio_comarea 	Ratio of commercial buildings in a give region
Buildings 	ratio_resarea 	Ratio of residential buildings in a give region
Buildings 	ratio_officerea 	Ratio of office buildings in a give region
Buildings 	avg_numfloors 	The average number of floors
Buildings 	total_bldgarea 	Total building area
Census 	total_population 	Total population
Census 	family_households 	family households
Census 	household_type_by_units_in_structure 	household type by units in structure
Census 	households_income 	households income
Census 	average_household_size_of_occupied_housing_units 	average household size of occupied housing units
Census 	total_housing_units 	Total housing units
Census 	median_number_of_rooms 	Median number of rooms
Census 	median_contract_rent 	Median contract rent
Census 	median_gross_rent 	Median gross rent
Census 	median_household_income 	Median household income
Census 	aggregate_household_income 	Aggregated household income
Census 	owner_occupied_homes_median_value 	Owner occupied homes median value
Census 	value_for_owner_occupied_housing_units 	Median value for owner occupied housing units
Census 	owner_occupied_homes_median_value 	Owner occupied homes median value
Census 	total_vacancies 	Total vacancies appartements
Census 	sold_not_occupied 	Sold non-occupied appartements
Census 	for_rent 	Appartements for rent
Census 	median_age 	Media age
Census 	population_5_and_over 	Population ages 5-18
Census 	adults_18_to_20 	Population ages 18-20
Census 	adults_25_to_64 	Population ages 25-64
Census 	adults_25_to_64_with_bachelors_degree 	Population ages 25-64 with bechelor degree
Census 	below_poverty_line 	Population below poverty line
Census 	foreign_born_population 	Foreign-born population
Census 	people_per_household 	Number of persons per household
Census 	built_total 	Average of buildings age
Census 	built_1970s 	Number of buildings built on 1970s
Census 	built_1960s 	Number of buildings built on 1960s
Census 	built_1950s 	Number of buildings built on 1950s
Census 	built_1940s 	Number of buildings built on 1940s
Census 	built_before_1940 	Number of buildings built before 1940s
Census 	median_household_income 	Media household income
Census 	poverty_level_u100 	Poverty level
Code Strucutre

The project is structured in the following components:

    FireCaster_Model : Build and validate the model

    data_acquisition: contains scripts to download the data

    data_processing: contains scripts for our process of crawling and transforming the data to a usable format.

    data_analysis: contains scripts for supporting tasks carried out throughout the process of building the fire risk model.

    FireCaster_Dashboard: Map-centered web application to visualize the results. We run a cron-job to generate scores and read the scores directly from DB.
