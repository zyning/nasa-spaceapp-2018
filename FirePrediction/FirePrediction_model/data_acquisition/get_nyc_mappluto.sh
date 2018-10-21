#!/bin/bash
BASEDIR=$(dirname "$0")

NYC_RAW_DIR="../data/raw"
NYC_INTREIM_DIR="../data/intreim"
NYC_PROCESSED_DIR="../data/processed"

ITEM_NAME="MapPluto"
CONFIG_FILE="../config/data_sources.json"

REGX_PASS='.CONTEXTUAL_DATA[] | select(.NAME=="'$ITEM_NAME'")'
NYC_MAPPLUTO_URL="$(cat "$CONFIG_FILE" | jq "$REGX_PASS" | jq ".URLs[0]" | tr -d '"' )"

echo $NYC_MAPPLUTO_URL
#VERSIONS=( "16v1" "15v1" "14v2" "14v1" "13v2" "13v1" "12v2" "12v1" "11v2" "11v1" "10v2" "10v1" "09v2" "09v1" "07c" "06c" "05d" "04c" "03c" "02a" )
VERSIONS=( "16v1" )
EXT=".zip"
NYC_BOUROUGHS=( "Bronx" "Brooklyn" "Manhattan" "Queens" "Staten_Island" )

# # create folder if it doesn't exist
if [ ! -e $NYC_RAW_DIR ]; then mkdir -p $NYC_RAW_DIR; fi
if [ ! -e $NYC_INTREIM_DIR ]; then mkdir -p $NYC_INTREIM_DIR; fi
if [ ! -e $NYC_PROCESSED_DIR ]; then mkdir -p $NYC_PROCESSED_DIR; fi

# # # Create new folder

for version in "${VERSIONS[@]}"
do
  #if [ ! -e $NYC_INTREIM_DIR/$version ]; then mkdir -p $NYC_INTREIM_DIR/$version; fi 
  if [ ! -e $NYC_PROCESSED_DIR/$version ]; then mkdir -p $NYC_PROCESSED_DIR/$version; fi 
done

# Download files from NYC Gov website : http://www1.nyc.gov/site/planning/data-maps/open-data/pluto-mappluto-archive.page
echo "Downloading files"
for version in "${VERSIONS[@]}"
do
  wget -O $NYC_RAW_DIR/"mappluto_"$version$EXT $NYC_MAPPLUTO_URL$version$EXT
done

echo "Unzip files"
for version in "${VERSIONS[@]}"
do
  unzip $NYC_RAW_DIR/"mappluto_"$version$EXT *PLUTO.shp -d $NYC_INTREIM_DIR/$version/
  unzip $NYC_RAW_DIR/"mappluto_"$version$EXT *.shx -d $NYC_INTREIM_DIR/$version/
  unzip $NYC_RAW_DIR/"mappluto_"$version$EXT *.dbf -d $NYC_INTREIM_DIR/$version/
done

echo "Merge the files into one file"
for version in "${VERSIONS[@]}"
do
  OUTPUT_FILE="$NYC_PROCESSED_DIR/$version/nyc_map_pluto_$version.shp"
  FILE_SUFFIX="nyc_map_pluto_$version"
  for filei in `find $NYC_INTREIM_DIR/$version -name "*.shp" -print`
  do
    if [ -f "$OUTPUT_FILE" ]
      then
        ogr2ogr -f 'ESRI Shapefile' -s_srs EPSG:2263 -t_srs EPSG:4326 -skipfailures -update -append $OUTPUT_FILE $filei -nln $FILE_SUFFIX
      else
        ogr2ogr -f 'ESRI Shapefile' -s_srs EPSG:2263 -t_srs EPSG:4326 -skipfailures $OUTPUT_FILE $filei
    fi
  done
done

# # Checking the merged file
for filename in $NYC_PROCESSED_DIR/$version/*.shp; do
  ogrinfo -al -so $filename
done

# # # Convert files to SQL
for filei in `find $NYC_PROCESSED_DIR/$version -name "*.shp" -print`
do
  SRC_TABLE=`basename $filei .shp`""
  FILE_SUFFIX=`basename $filei .shp`".sql"
  OUTPUT_FILE="$NYC_PROCESSED_DIR/$FILE_SUFFIX"
  shp2pgsql -a -s 2263 -D -g geom -N abort $filei $SRC_TABLE >> $OUTPUT_FILE
done

# # Convert files to Geojson, this is in case you want to load it to other databases
for filei in `find $NYC_PROCESSED_DIR/$version -name "*.shp" -print`
do
  FILE_SUFFIX=`basename $filei .shp`".geojson"
  echo $filei

  ogr2ogr -f GeoJSON $NYC_PROCESSED_DIR/$FILE_SUFFIX $filei
done



