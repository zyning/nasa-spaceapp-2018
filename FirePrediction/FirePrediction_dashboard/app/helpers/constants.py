# Path to Configuration file
CONFIG_DIR = './app/config'
CONFIG_DB = 'db.json'

QUERY_FETCH_NYC_TRACTS = "select nyc_tracts from fire_predictions;"
QUERY_FETCH_NYC_TRACT = "select nyc_tracts from fire_predictions WHERE nyc_tracts -> 'tract_id' == {};"