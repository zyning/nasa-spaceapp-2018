#!/bin/bash
BASEDIR=$(dirname "$0")

NYC_RAW_DIR="../data/raw"
NYC_INTREIM_DIR="../data/intreim"
NYC_PROCESSED_DIR="../data/processed"
DB_NAME="firecaster_db"
DB_USERNAME=""
DB_HOSTNAME=""

#PSQL="psql -h $DB_HOSTNAME -U $DB_USERNAME $DB_NAME"
PSQL="psql -d $DB_NAME"


# Import Weather Data
cat $NYC_PROCESSED_DIR/nyc_weather_filtered.csv | sed 's/;[^;]*$//' | ${PSQL} -c "copy nyc_weather from stdin DELIMITER E'\t' CSV HEADER"

# Import Incident Data
cat $NYC_PROCESSED_DIR/nyc_fire_incidents_out.csv | cut -f1,4,14,33 | sed 's/;[^;]*$//' | ${PSQL} -c "copy nyc_fire_incident from stdin DELIMITER E'\t' CSV HEADER"

# Import NYC Census Tracts
cat $NYC_PROCESSED_DIR/nyc_tracts.csv | sed 's/;[^;]*$//' | ${PSQL} -c "copy nyc_census from stdin DELIMITER E'\t' CSV HEADER"

# Import NYC Mappluto Data
${PSQL} -f $NYC_PROCESSED_DIR/nyc_map_pluto_16v1.sql #-v ON_ERROR_STOP=1

# Import NYC Street segments 
${PSQL} -f $NYC_PROCESSED_DIR/nyc_streets_segments.sql #-v ON_ERROR_STOP=1

