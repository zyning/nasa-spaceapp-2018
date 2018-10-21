# Path to Configuration file
CONFIG_DIR = './config'
CONFIG_DB = 'db.json'

# Fields
DATETIME_FIELD = u'incident_date_time'

TEST_PERIOD = ['{}-12-2014'.format(str(i).zfill(2)) for i in range(31)]

# Commands to run the script
RUN_TASK_SHUFFLE_VALIDATION = False
RUN_TASK_OUT_TIME_VALIDATION = True 
RUN_DATA_AGGREGATION_TASK = 'DATA_AGGREGATION'
RUN_DATA_PREPROCESSING_TASK = 'DATA_PREPROCESSING'
RUN_DATA_CLEANING_TASK = 'DATA_CLEANING'
RUN_CONTEXTUAL_DATA_COLLECTION_TASK = 'CONTEXTUAL_DATA_COLLECTION'
RUN_FEATURE_ENGINEERING_TASK = 'FEATURE_ENGINEERING'
RUN_MODEL_SELECTION_TASK = 'MODEL_SELECTION'
RUN_SCHEDULER_TASK = 'SCHEDULER'
RUN_ALL_TASKS = 'ALL'

# Path to directories 
RAW_DIR="./data/raw"
INTERIM_DIR="./data/intreim"
PROCESSED_DIR="./data/processed"

# Fire Incidents input/output files 
NYC_FIRE_INCIDENTS_FNAME = "nyc_fire_incidents.csv"
NYC_FIRE_INCIDENTS_FNAME_OUT = "nyc_fire_incidents_out.csv"
NYC_MAPPLUTO_FILTERED_FNAME = "nyc_mappluto_filtered_data.csv"
NYC_MAPPLUTO_AGG_FNAME = "nyc_mappluto_agg_data.csv"

NYC_BUILDINGS_FOOTPRINTS_FNAME = "nyc_bin_bbl_tract.csv"
NYC_DOB_COMPLAINTS_FNAME = "nyc_dob_complaints.csv"
NYC_DOB_PERMITS_FNAME = "nyc_dob_permits.csv"
NYC_DOB_VIOLATIONS_FNAME = "nyc_dob_violations.csv"
NYC_ECB_VIOLATIONS_FNAME = "nyc_dob_ecb_violations.csv"
NYC_DOB_AGG_FNAME =  "nyc_dob_complaints_agg.csv"

NYC_DOB_COMPLAINTS_AGG_FNAME = "nyc_dob_complaints_agg.csv"
NYC_DOB_ECB_VIOLATIONS_AGG_FNAME = "nyc_dob_ecb_violations_agg.csv"
NYC_DOB_PERMITS_AGG_FNAME = "nyc_dob_permits_agg.csv"

NYC_FIRE_INCIDENTS_SPARSE_FNAME = "nyc_fire_incidents_sp.csv"
NYC_FIRE_INCIDENTS_TRACTS_FNAME = "nyc_fire_incidents_tracts.csv"
NYC_FIRE_INCIDENTS_TRACTS_BYDAY_FNAME = "nyc_fire_incidents_tracts_day.csv"
NYC_INCIDENTS_TRACTS_CENSUS_FNAME = "nyc_fire_incidents_tracts_census.csv"
NYC_INCIDENTS_TRACTS_CENSUS_WEATHER_FNAME = "nyc_fire_incidents_tracts_census_weather.csv"
NYC_INCIDENTS_TRACTS_CONTEXT_FNAME = "nyc_fire_incidents_tracts_context.csv"
NYC_WEATHER_FNAME =  "nyc_weather_filtered.csv"
NYC_INCIDENTS_CONTEXT_FINAL_FNAME = "nyc_fire_incidents_tracts_context_final.csv"

# NYC streets input/output files
NYC_STREETS_FNAME = "StreetSegment.csv"
NYC_STREETS_OUT = "nyc_streets_segments"
NYC_STREETS_SEGMENTS_FNAME = "_nyc_streets_segments.csv"

RF_CLR_FNAME = 'rf_classifier_firecaster.p'

# e.g: 01/01/2013 12:00:20 AM
INCIDENT_TIME_FORMAT ='%m/%d/%Y %I:%M:%S %p'
# e.g: 01-01-2013
DAY_TIME_FORMAT = '%d-%m-%Y'
# e.g: 06/08/2011
COMPLAINT_FORMAT = '%m/%d/%Y'
# e.g: 06/08/2011
VIOLATION_FORMAT = '%Y%m%d'


# standard time format
STANDARD_TIME_FORMAT = '%d-%m-%Y'
STANDARD_TIME_FORMAT_M = '%m-%Y'
STANDARD_TIME_FORMAT_Y = '%Y'
STANDARD_TIME_FORMAT_H = '%d-%m-%YT%H'

NULL = "null"

# Demographics, tract-level income and poverty, employment and education, county-level income
# https://api.census.gov/data/2010/acs5/variables.json

CENSUS_FIELDS = {  
	# people 
	"B01001_001E": "total_population",
	# "B00002_001E": "unweighted_sample_housing_units",

	# building 
	"B11001_002E": "family_households",
	"B11011_001E": "household_type_by_units_in_structure",
	"B19001_001E": "households_income",
	"B25010_001E": "average_ousehold_size_of_occupied_housing_units",
	"B25001_001E": "total_housing_units",
	"B25021_001E": "median_number_of_rooms", 
	"B25058_001E": "median_contract_rent", 
	"B25064_001M": "median_gross_rent",
	"B19013_001E": "median_household_income",
	"B19025_001E": "aggregate_household_income",
	"B25077_001E": "owner_occupied_homes_median_value",
	"B25075_025E": "value_for_owner_occupied_housing_units", 

	# neighberhood
	"B25004_001E": "total_vacancies",
	"B25004_005E": "sold_not_occupied",
	"B25004_002E": "for_rent",

	# age 
	"B01002_001E": "median_age",
	"B16001_001E": "population_5_and_over",
	"B23003_001E": "adults_18_to_20",
	"B23006_001E": "adults_25_to_64",
	"B23006_001E": "adults_25_to_64_with_bachelors_degree",
	"B06012_002E": "below_poverty_line",

	# ethnicity and 
	"B06001_049E": "foreign_born_population",
	"B25010_001E": "people_per_household", 

	"B02001_002E": "white_pop",
	"B02001_003E": "black_pop",
	"B01001I_001E": "hispanic_pop",
	"B02001_005E": "asian_pop",
	"B02001_006E": "pacific_pop",
	"B02001_004E": "native_pop",
	"B02001_007E": "older_pop",

	# year structure was built
	'B25034_001E': 'built_total',
	'B25034_006E': 'built_1970s',
	'B25034_007E': 'built_1960s',
	'B25034_008E': 'built_1950s',
	'B25034_009E': 'built_1940s', 
	'B25034_010E': 'built_before_1940',

	## at risk groups as defined by the cdc
	'B01001_003E': 'm_u5', 
	'B01001_027E': 'f_u5',


	'B01001B_003E': 'm_u5_black',
	'B01001B_027E': 'f_u5_black',
	'B01001C_003E': 'm_u5_indig',
	'B01001C_027E': 'f_u5_indig', 
	'B01001H_003E': 'm_u5_latin',
	'B01001H_027E': 'f_u5_latin',

	'B05009_012E': 'foreign_parents_u6', 
	'B05009_012E': 'one_foreign_parent_one_us_parent_u6_foreign',
	'B05009_009E': 'foreign_parents_u6_foreign',
	'B05009_019E': 'one_foreign_parent_u6_foreign',
	'B05009_005E': 'foreign_born_child',

	'B06012_002E': 'poverty_level_u100',
	'B06012_003E': 'poverty_level_u149_o100',

	# income 
	"B19013_001E": "median_household_income"

	# 'B19001_002E': 'households income < 10k',
	# 'B19001_003E': 'households income 10k-15k',
	# 'B19001_004E': 'households income 15k-20k',
	# 'B19001_005E': 'households income 20k-25k',
	# 'B19001_006E': 'households income 25k-30k',
	# 'B19001_007E': 'households income 30-35k',
	# 'B19001_008E': 'households income 35-40k',
	# 'B19001_009E': 'households income 40-45k',
	# 'B19001_010E': 'households income 45-50k',
	# 'B19001_011E': 'households income 50-60k',
	# 'B19001_012E': 'households income 60-75k',
	# 'B19001_013E': 'households income 75-100k',
	# 'B19001_014E': 'households 100-125k',
	# 'B19001_015E': 'households 125-150k',
	# 'B19001_016E': 'households 150-200k',
	# 'B19001_017E': 'households 200k+'
}

SPATIAL_UNIT  = 'all'

# Dictionaries to standarize street names 
DESIGNATORS = {"Apt": "Appartment", "Bld": "Building", "Ste": "Suite", "Rm": "Room", "Fl": "Floor", "Un": "Unit", "Flr": "Floor"}
MAPPING_STREETS = {'BD': 'BOULEVARD', 'WF': 'WARF', 'HY': 'HIGHWAY', 'GA': 'GATE', 'WA': 'WAY', 'BL': 'BOULEVARD', 'TER': 'TERRACE', 'WK': 'WALK', 'CIR': 'CIRCLE', 'GEO': 'GEORGE', 'CV': 'COVE', 'BLVD': 'BOULEVARD', 'CO': 'COMMON', 'DR': 'DRIVE', 'WY': 'WAY', 'LD': 'LANDING', 'PW': 'PARKWAY', 'PT': 'POINT', 'LA': 'LANE', 'LN': 'LANE', 'LO': 'LOOP', 'TR': 'TRAIL', 'NE': 'NORTH EAST', 'TP': 'TURNPIKE', 'PKWY': 'PARKWAY', 'RD': 'ROAD', 'TL': 'TRAIL', 'SH': 'SHOALS', 'TK': 'TURNIPKE', 'HWY': 'HIGHWAY', 'PK': 'PARKWAY', 'RN': 'RUN', 'TE': 'TERRACE', 'RH': 'REACH', 'PO': 'POST', 'PL': 'PLACE', 'NW': 'NORTH WEST', 'CI': 'CIRCLE', 'CH': 'CHASE', 'E': 'EAST', 'TRL': 'TRAIL', 'CM': 'COMMONS', 'CL': 'CLOSE', 'CG': 'CROSSING', 'N': 'NORTH', 'CZ': 'CROSS', 'S': 'SOUTH', 'AR': 'ARCH', 'EX': 'EXTENSION', 'W': 'WEST', 'AV': 'AVENUE', 'CS': 'CRESCENT', 'CR': 'CIRCLE', 'CW': 'CAUSEWAY', 'CT.': 'CENTER', 'CT': 'CENTER', 'GDNS': 'GARDENS', 'QU': 'QUAY', 'TC': 'TRACE', 'SQ': 'SQUARE', 'CRES': 'CRESCENT', 'SW': 'SOUTH WEST', 'ST': 'STREET', 'PZ': 'PLAZA', 'ARC': 'ARCH', 'MS': 'MUSE', 'W.': 'WEST', 'SC': 'SHOPPING CENTER', 'AVE': 'AVENUE', 'KY': 'KEY', 'SE': 'SOUTH EAST'}

# Page 39: https://www1.nyc.gov/assets/planning/download/pdf/data-maps/open-data/pluto_datadictionary.pdf?v=16v2
BORO_CODE = {'1':'36061','2':'36005','3':'36047','4':'36081','5':'36085'}
BORO_STR_CODE = {'MANHATTAN':'1','BRONX':'2','BROOKLYN':'3','QUEENS':'4','STATEN ISLAND':'5'}

# Regions
NYC_REGION = "NY"
NYC_CITY = "New_York" 

# Weather Data
WUNDERGROUND_KEYS_FNAME = "wunderground_keys.json"
NYC_WEATHER_INFO_FNAME = "newyork_weather_info.csv"
NYC_WEATHER_FILTERED_FNAME =  "newyork_weather_filtered.csv"

# ACS5 Census Data
ACS5_TABLE_ID = 'acs5'
ACS5_YEAR = 2015
SPATIAL_UNIT_TRACT = {'granularity': 'tract', 'state': '36' ,  'tract': '*' }
SPATIAL_UNIT_BLOCK = {'granularity': 'blockgroup', 'state': '36' ,  'tract': '*', 'blockgroup': '*' }

NYC_TRACTS_FNAME = "nyc_tracts.csv" 
NYC_BLOCKS_FNAME = "nyc_blocks.csv"

RELEVANT_FEATURES = [u'incident_date_time', u'census_tract', u'nbr_incidents', 
		'wday_mon', 'wday_tue', 'wday_wed', 'wday_thu', 'wday_fri', 'wday_sat', 'wday_sun', 
		'month_jan', 'month_feb', 'month_mar', 'month_apr', 'month_may', 'month_jun', 'month_jul', 'month_aug', 'month_sep', 'month_oct', 'month_nov', 'month_dec',
       u'population_5_and_over', u'f_u5', u'older_pop', u'built_total',
       u'f_u5_latin', u'black_pop', u'household_type_by_units_in_structure',
       u'built_1940s', u'built_before_1940', u'built_1950s', u'built_1960s', u'built_1970s', u'adults_18_to_20',
       u'adults_25_to_64_with_bachelors_degree', u'white_pop',
       u'people_per_household', u'm_u5_latin', u'median_gross_rent',
       u'm_u5_indig', u'owner_occupied_homes_median_value',
       u'family_households', u'pacific_pop', u'aggregate_household_income',
       u'households_income', u'total_housing_units',
       u'for_rent', u'm_u5', u'one_foreign_parent_one_us_parent_u6_foreign',
       u'value_for_owner_occupied_housing_units',
       u'one_foreign_parent_u6_foreign', u'median_household_income',
       u'f_u5_indig', u'median_number_of_rooms', u'asian_pop',
       u'total_vacancies', u'median_age', u'sold_not_occupied',
       u'foreign_born_child', u'foreign_born_population', u'hispanic_pop',
       u'foreign_parents_u6_foreign', u'poverty_level_u149_o100',
       u'poverty_level_u100', u'total_population', u'm_u5_black',
       u'native_pop', u'median_contract_rent', u'f_u5_black', u'mintempm',
       u'maxtempm', u'snowdepthm', u'meanpressurem',
       u'meanwindspdm', u'precipm',  u'nbr_ecb_violations',
       u'nbr_dob_violations', u'nbr_dob_permits', 
       u'avg_unitsres', u'ratio_retailarea', u'ratio_resarea', u'ratio_comarea', 
       u'avg_yearbuilt', u'ratio_officerea', u'avg_numfloors', u'total_units', 
       u'avg_unitarea', u'total_bldgarea']


PREDICTORS = ['wday_mon', 'wday_tue', 'wday_wed', 'wday_thu', 'wday_fri', 'wday_sat', 'wday_sun', 
		'month_jan', 'month_feb', 'month_mar', 'month_apr', 'month_may', 'month_jun', 'month_jul', 'month_aug', 'month_sep', 'month_oct', 'month_nov', 'month_dec',
       u'population_5_and_over', u'f_u5', u'older_pop', u'built_total',
       u'f_u5_latin', u'black_pop', u'household_type_by_units_in_structure',
       u'built_1940s', u'built_before_1940', u'built_1950s', u'built_1960s', u'built_1970s', u'adults_18_to_20',
       u'adults_25_to_64_with_bachelors_degree', u'white_pop',
       u'people_per_household', u'm_u5_latin', u'median_gross_rent',
       u'm_u5_indig', u'owner_occupied_homes_median_value',
       u'family_households', u'pacific_pop', u'aggregate_household_income',
       u'households_income', u'total_housing_units',
       u'for_rent', u'm_u5', u'one_foreign_parent_one_us_parent_u6_foreign',
       u'value_for_owner_occupied_housing_units',
       u'one_foreign_parent_u6_foreign', u'median_household_income',
       u'f_u5_indig', u'median_number_of_rooms', u'asian_pop',
       u'total_vacancies', u'median_age', u'sold_not_occupied',
       u'foreign_born_child', u'foreign_born_population', u'hispanic_pop',
       u'foreign_parents_u6_foreign', u'poverty_level_u149_o100',
       u'poverty_level_u100', u'total_population', u'm_u5_black',
       u'native_pop', u'median_contract_rent', u'f_u5_black', u'mintempm',
       u'maxtempm', u'snowdepthm', u'meanpressurem',
       u'meanwindspdm', u'precipm',  
       u'avg_unitsres', u'ratio_retailarea', u'ratio_resarea', u'ratio_comarea', 
       u'avg_yearbuilt', u'ratio_officerea', u'avg_numfloors', u'total_units', 
       u'avg_unitarea', u'total_bldgarea']

TARGET = u'nbr_incidents'
