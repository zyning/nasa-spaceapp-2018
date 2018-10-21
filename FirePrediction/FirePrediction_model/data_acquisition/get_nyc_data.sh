#!/bin/bash
NYC_RAW_DIR="../data/raw"
NYC_INTREIM_DIR="../data/intreim"
NYC_PROCESSED_DIR="../data/processed"


CONFIG_FILE="../config/data_sources.json"
#CONTEXTUAL_DATA_FNAMES=( "MapPluto" "NYC_tracts" "CENSUS_ACS_2015" "DOB_complaints" "DOB_violations" "DOB_ecb_violations" "NYC_311_complaints" )
CONTEXTUAL_DATA_FNAMES=( "NYC_streets" ) # "NYC_tracts" "CENSUS_ACS_2015" "DOB_complaints" "DOB_violations" "DOB_ecb_violations" )
FIRE_INCIDENTS_DATA_FNAMES=( "NYC")
DATA_FILES_TO_PROCESS=( "NYC_streets" "NYC_geo_tracts" )

# Getting contextual datasets
for item_name in "${CONTEXTUAL_DATA_FNAMES[@]}" "${FIRE_INCIDENTS_DATA_FNAMES[@]}";
do
	REGX_PASS='.CONTEXTUAL_DATA[] | select(.NAME=="'$item_name'")'
	NYC_ITEM_URL="$(cat "$CONFIG_FILE" | jq "$REGX_PASS" | jq ".URLs[0]" | tr -d '"' )"
	NYC_ITEM_FNAME="$(cat "$CONFIG_FILE" | jq "$REGX_PASS" | jq ".FNAME" | tr -d '"' )"

	# Download the file and store it in the RAW directory
	echo "Downloading: ", $NYC_ITEM_FNAME
	wget -O $NYC_RAW_DIR/$NYC_ITEM_FNAME $NYC_ITEM_URL
done

# Getting city's fire incidents' data
for item_name in "${FIRE_INCIDENTS_DATA_FNAMES[@]}";
do
	REGX_PASS='.FIRE_INCIDENTS[] | select(.NAME=="'$item_name'")'
	NYC_ITEM_URL="$(cat "$CONFIG_FILE" | jq "$REGX_PASS" | jq ".URLs[0]" | tr -d '"' )"
	NYC_ITEM_FNAME="$(cat "$CONFIG_FILE" | jq "$REGX_PASS" | jq ".FNAME" | tr -d '"' )"

	# Download the file and store it in the RAW directory
	echo "Downloading: ", $NYC_ITEM_FNAME
	wget -O $NYC_RAW_DIR/$NYC_ITEM_FNAME $NYC_ITEM_URL
done

# Transforming 
for item_name in "${DATA_FILES_TO_PROCESS[@]}"
do
	REGX_PASS='.CONTEXTUAL_DATA[] | select(.NAME=="'$item_name'")'
	ITEM_FNAME="$(cat "$CONFIG_FILE" | jq "$REGX_PASS" | jq ".FNAME" | tr -d '"' )"
	ITEM_DIR="$(cat "$CONFIG_FILE" | jq "$REGX_PASS" | jq ".DIR" | tr -d '"' )"
	
	# Unzip the tract file
	unzip $NYC_RAW_DIR/$ITEM_FNAME -d $NYC_INTREIM_DIR/$ITEM_DIR/$ITEM_NAME

	# Find the name of the unzipped file
	filei="$(find $NYC_INTREIM_DIR/$ITEM_NAME/$ITEM_DIR/ -name "*.shp" -print)"
	NYC_SHP_FNAME=`basename $filei .shp`""

	# Convert to GeoJSON
	# echo "Preparing GeoJSON file for item: ", $ITEM_NAME
	ogr2ogr -f GeoJSON $NYC_INTREIM_DIR/$NYC_SHP_FNAME".geojson" $filei

	# # # convert to SQL
	# echo "Preparing SQL file for item: ", $ITEM_NAME 
	# shp2pgsql -a -s 2263 -D -g geom -N abort $filei $ITEM_NAME >> $NYC_SQL_DIR/$ITEM_NAME."sql"

	# echo "Preparing CSV file for item: ", $ITEM_NAME 
	ogr2ogr -f "CSV" -t_srs EPSG:4326 -lco GEOMETRY=AS_WKT $NYC_INTREIM_DIR/$NYC_SHP_FNAME".csv" $filei

done
