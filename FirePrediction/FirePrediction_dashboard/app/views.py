from flask import render_template, Response, flash, redirect, url_for, request, abort, jsonify, stream_with_context, \
    make_response
from app import *
from app.db.db_connector import MongoDBConnector
from app.helpers.constants import CONFIG_DIR, CONFIG_DB, QUERY_FETCH_NYC_TRACT, QUERY_FETCH_NYC_TRACTS
import json 
from os.path import abspath, join, dirname

# # Load configuration file
# path_config = abspath(join(CONFIG_DIR, CONFIG_DB))
# CONFIG =  json.loads(open(path_config).read())

# # DB Connection 
# db_connector = MongoDBConnector(CONFIG)

#
@app.route('/')
@app.route('/nyc/')
def index():
    return render_template("index.html")

@app.route('/get_city_preds/', methods=['GET', 'POST'])
def get_city_preds():
	records = db_connector.run_query(QUERY_FETCH_NYC_TRACTS)
	return jsonify(records)

@app.route('/get_tract_preds/<tract_id>', methods=['GET', 'POST'])
def get_tract_preds(tract_id):
	records = db_connector.run_query(QUERY_FETCH_NYC_TRACT.format(tract_id))
	return jsonify(records)
