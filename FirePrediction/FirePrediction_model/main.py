from data_acquisition.services.weather_info_collector import WeatherInfoCollector
from data_acquisition.services.census_client import CensusAPIClient
from data_analysis.data_analyzer import DataAnalyzer
from db.db_connector import DBConnector
from data_processing.data_quester import DataQuester
from data_processing.data_transformer import DataTransformer
from sklearn.ensemble import RandomForestClassifier
from os.path import abspath, join, dirname
from resources.constants import *
from config.keys import CENSUS_KEY
from config.parameters import EXPERIMENT_START_DATE, EXPERIMENT_END_DATE
import numpy as np
import json
import logging
import argparse

if __name__ == '__main__':
    # # ---------------------------------
    # # Configuration File
    # # ---------------------------------

    parser = argparse.ArgumentParser(description='FireCaster Model Builder')
    parser.add_argument('-task', help='Please provide the name of the task', required=False)
    args = vars(parser.parse_args())
    RUN_TASK = args['task']

    # Load DB Configuration
    db_config = json.loads(open(abspath(join(CONFIG_DIR, CONFIG_DB))).read())

    logging.basicConfig(level=logging.INFO)
    CURRENT_LOC = dirname(__file__)

    # # # ---------------------------------
    # # # 1 - Contextual Data Collection
    # # # ---------------------------------

    if (RUN_TASK == RUN_ALL_TASKS) or (RUN_TASK == RUN_CONTEXTUAL_DATA_COLLECTION_TASK):
        # # Get Weather Data
        logging.info("Get Weather Data")
        wunderground_keys_fname = abspath(join(CONFIG_DIR, WUNDERGROUND_KEYS_FNAME))
        weather_collector = WeatherInfoCollector(start_date=EXPERIMENT_START_DATE, end_date=EXPERIMENT_END_DATE)
        output_fname = abspath(join(INTERIM_DIR, NYC_WEATHER_INFO_FNAME))
        weather_collector.get_weather_info_period(wunderground_keys_fname, output_fname, region=NYC_REGION,
                                                  city=NYC_CITY)

        # Get Census Data
        logging.info("Get Census Data")
        output_fname = abspath(join(PROCESSED_DIR, NYC_TRACTS_FNAME))
        census_api_client = CensusAPIClient(year=ACS5_YEAR, data_id=ACS5_TABLE_ID, var_list=CENSUS_FIELDS.keys(),
                                            table_id=ACS5_TABLE_ID, spatial_unit='all', key=CENSUS_KEY)
        census_api_client.get_census_data(spatial_unit=SPATIAL_UNIT_TRACT, fname=output_fname)

        # Filter & Export Data
        logging.info("Filter & Export Data")
        mappluto_fname = abspath(join(PROCESSED_DIR, NYC_MAPPLUTO_FILTERED_FNAME))
        db_connector = DBConnector(db_config)
        data_quester = DataQuester(db_connector)
        data_quester.get_mappluto_data(mappluto_fname)

    # # # ---------------------------------
    # # # 2 - Data Preprocessing 
    # # # ---------------------------------

    if (RUN_TASK == RUN_ALL_TASKS) or (RUN_TASK == RUN_DATA_PREPROCESSING_TASK):
        db_connector = DBConnector(db_config)
        data_quester = DataQuester(db_connector)
        data_normalizer = DataTransformer()

        # normalize NYC indcidents data
        logging.info("normalize NYC indcidents data")
        nyc_incidents_input_fname = abspath(join(RAW_DIR, NYC_FIRE_INCIDENTS_FNAME))
        nyc_incidents_fname = abspath(join(PROCESSED_DIR, NYC_FIRE_INCIDENTS_FNAME_OUT))
        data_normalizer.normalize_nyc_incidents_file(nyc_incidents_input_fname, nyc_incidents_fname)

        # normalize streets 
        logging.info("normalize streets")
        nyc_streets_input_fname = abspath(join(INTERIM_DIR, NYC_STREETS_FNAME))
        nyc_streets_fname = abspath(join(PROCESSED_DIR, NYC_STREETS_OUT))
        data_normalizer.normalize_street_file(nyc_streets_input_fname, nyc_streets_fname)

        # filter weather data
        logging.info("filter weather data")
        weather_collector = WeatherInfoCollector(start_date=EXPERIMENT_START_DATE, end_date=EXPERIMENT_END_DATE)
        weather_input_fname = abspath(join(INTERIM_DIR, NYC_WEATHER_INFO_FNAME))
        weather_fname = abspath(join(PROCESSED_DIR, NYC_WEATHER_FILTERED_FNAME))
        weather_collector.filter_weather_data(weather_input_fname, weather_fname)

        # aggregate/average mappluto data
        logging.info("aggregate/average mappluto data")
        mappluto_fname = abspath(join(PROCESSED_DIR, NYC_MAPPLUTO_FILTERED_FNAME))
        mappluto_agg_fname = abspath(join(PROCESSED_DIR, NYC_MAPPLUTO_AGG_FNAME))
        data_normalizer.aggregate_mappluto(mappluto_fname, mappluto_agg_fname)

        # nyc building footprints 
        nyc_buildings_fname = abspath(join(PROCESSED_DIR, NYC_BUILDINGS_FOOTPRINTS_FNAME))

        # aggregate/average DOB complaints 
        logging.info("aggregate/average DOB complaints")
        dob_complaints_fname = abspath(join(PROCESSED_DIR, NYC_DOB_COMPLAINTS_FNAME))
        dob_complaints_agg_fname = abspath(join(PROCESSED_DIR, NYC_DOB_COMPLAINTS_AGG_FNAME))
        data_normalizer.aggregate_complaints_data(nyc_buildings_fname, dob_complaints_fname, dob_complaints_agg_fname)

        # aggregate/average DOB/ECB permits
        logging.info("aggregate/average DOB/ECB permits")
        ecb_violations_fname = abspath(join(PROCESSED_DIR, NYC_ECB_VIOLATIONS_FNAME))
        dob_violations_fname = abspath(join(PROCESSED_DIR, NYC_DOB_VIOLATIONS_FNAME))
        dob_ecb_violations_agg_fname = abspath(join(PROCESSED_DIR, NYC_DOB_ECB_VIOLATIONS_AGG_FNAME))
        data_normalizer.aggregate_violations_data(nyc_buildings_fname, dob_violations_fname, ecb_violations_fname,
                                                  dob_ecb_violations_agg_fname)

        # aggregate/average DOB permits 
        logging.info("aggregate/average DOB permits")
        dob_permits_fname = abspath(join(PROCESSED_DIR, NYC_DOB_PERMITS_FNAME))
        dob_permits_agg_fname = abspath(join(PROCESSED_DIR, NYC_DOB_PERMITS_AGG_FNAME))
        data_normalizer.aggregate_permits_data(nyc_buildings_fname, dob_permits_fname, dob_permits_agg_fname)

    # # # ---------------------------------
    # # # 2 - Data Processing / Feature Engineering
    # # # ---------------------------------

    if (RUN_TASK == RUN_ALL_TASKS) or (RUN_TASK == RUN_FEATURE_ENGINEERING_TASK):
        data_transformer = DataTransformer()

        # join incidents to tracts
        logging.info("join incidents to tracts")
        incidents_fname = abspath(join(PROCESSED_DIR, NYC_FIRE_INCIDENTS_FNAME_OUT))
        street_fname = abspath(join(PROCESSED_DIR, NYC_STREETS_SEGMENTS_FNAME))
        incidents_tracts_fname = abspath(join(PROCESSED_DIR, NYC_FIRE_INCIDENTS_TRACTS_FNAME))
        data_transformer.join_with_tracts(incidents_fname, street_fname, incidents_tracts_fname)

        # flatten incidents/tracts
        logging.info("flatten incidents/tracts")
        incidents_tracts_fname = abspath(join(PROCESSED_DIR, NYC_FIRE_INCIDENTS_TRACTS_FNAME))
        nyc_census_fname = abspath(join(PROCESSED_DIR, NYC_TRACTS_FNAME))
        incidents_tracts_sp_fname = abspath(join(PROCESSED_DIR, NYC_FIRE_INCIDENTS_SPARSE_FNAME))
        data_transformer.flatten_incidents_tracts(incidents_tracts_fname, nyc_census_fname, incidents_tracts_sp_fname)

        # join incidents/tracts to Census
        logging.info("join incidents/tracts to Census")
        incidents_tracts_sp_fname = abspath(join(PROCESSED_DIR, NYC_FIRE_INCIDENTS_SPARSE_FNAME))
        nyc_census_fname = abspath(join(PROCESSED_DIR, NYC_TRACTS_FNAME))
        incidents_tracts_context_fname = abspath(join(PROCESSED_DIR, NYC_INCIDENTS_TRACTS_CONTEXT_FNAME))
        data_transformer.join_with_census_data(incidents_tracts_sp_fname, nyc_census_fname,
                                               incidents_tracts_context_fname)

        # join Incidents/Tracts/Census to Weather Data
        logging.info("join Incidents/Tracts/Census to Weather Data")
        weather_fname = abspath(join(PROCESSED_DIR, NYC_WEATHER_FNAME))
        data_transformer.join_with_weather_data(incidents_tracts_context_fname, weather_fname,
                                                incidents_tracts_context_fname)

        # join with mappluto data
        logging.info("join with mappluto data")
        mappluto_agg_fname = abspath(join(PROCESSED_DIR, NYC_MAPPLUTO_AGG_FNAME))
        data_transformer.join_with_mappluto_data(incidents_tracts_context_fname, mappluto_agg_fname,
                                                 incidents_tracts_context_fname)

        # join_complains_tracts
        logging.info("join complains_tracts")
        # aggregate/average DOB complaints
        dob_complaints_agg_fname = abspath(join(PROCESSED_DIR, NYC_DOB_COMPLAINTS_AGG_FNAME))
        data_transformer.join_with_complaints_data(incidents_tracts_context_fname, dob_complaints_agg_fname,
                                                   incidents_tracts_context_fname)

        # aggregate/average DOB/ECB permits
        logging.info("aggregate/average DOB/ECB permits")
        dob_ecb_violations_agg_fname = abspath(join(PROCESSED_DIR, NYC_DOB_ECB_VIOLATIONS_AGG_FNAME))
        data_transformer.join_with_violations_data(incidents_tracts_context_fname, dob_ecb_violations_agg_fname,
                                                   incidents_tracts_context_fname)

        # aggregate/average DOB permits
        logging.info("aggregate/average DOB permits")
        dob_permits_agg_fname = abspath(join(PROCESSED_DIR, NYC_DOB_PERMITS_AGG_FNAME))
        data_transformer.join_with_permits_data(incidents_tracts_context_fname, dob_permits_agg_fname,
                                                incidents_tracts_context_fname)

        # add time features 
        logging.info("add time features ")
        data_transformer.encode_time_features(incidents_tracts_context_fname)

        # rename columns 
        logging.info("rename columns")
        data_transformer.rename_columns(incidents_tracts_context_fname)

        # filter relevant features
        incidents_context_final_fname = abspath(join(PROCESSED_DIR, NYC_INCIDENTS_CONTEXT_FINAL_FNAME))
        data_transformer.filter_relevant_features(incidents_tracts_context_fname, incidents_context_final_fname)

    if (RUN_TASK == RUN_ALL_TASKS) or (RUN_TASK == RUN_MODEL_SELECTION_TASK):
        data_analyzer = DataAnalyzer()
        incidents_context_final_fname = abspath(join(PROCESSED_DIR, NYC_INCIDENTS_CONTEXT_FINAL_FNAME))

        # load data
        logging.info("load data")
        df_incidents_context = data_analyzer.load_data(incidents_context_final_fname)

        if (RUN_TASK_OUT_TIME_VALIDATION == True):
            # data spans from 01-01-2013 to 31-12-2014 
            # we run an experiment by training model on 01-01-2013 --> 31-11-2014  to predict next month 
            all_poss_dates =  np.unique(df_incidents_context[DATETIME_FIELD].values) 
            TRAIN_DATES = list(set(all_poss_dates) - set(TEST_PERIOD))
            for i in range(1, 31):
                prev_day = TEST_PERIOD[i-1]
                curr_day = TEST_PERIOD[i]
                logging.info("Predicting Day > {}".format(curr_day))
                TRAIN_DATES.append(prev_day)
                TEST_DATES = [curr_day]
                X_train, X_test, y_train, y_test = data_analyzer.train_test_split_chronologically(df_incidents_context, PREDICTORS, TARGET, TRAIN_DATES, TEST_DATES)
                classifier = RandomForestClassifier()
                data_analyzer.run_model(classifier, X_train, X_test, y_train, y_test)


        if (RUN_TASK_SHUFFLE_VALIDATION == True):
            # label target to infer whether this region might catch fire or no
            logging.info("encode target variable")
            df_incidents_context = data_analyzer.label_target(df_incidents_context, TARGET)

            # samples / target
            logging.info("get X, y")
            X, y = data_analyzer.load_samples(df_incidents_context, PREDICTORS, TARGET)

            # interpret features to fine-tune the model
            logging.info("calculate feature importance")
            data_analyzer.feature_importance(X, y, PREDICTORS)

            # After benchmarking different methods, decided to use Tree-based model - RandomForest 
            logging.info("Random Forest Classifier")
            classifier = RandomForestClassifier
            cv = 2  # number of folds
            logging.info("evaluating the model using k-folds: K= {}".format(cv))
            clr = data_analyzer.evaluate_model(X, y, classifier, cv)

            # dump_model
            clr_fname = abspath(join(PROCESSED_DIR, RF_CLR_FNAME))
            data_analyzer.dump_model(clr, clr_fname)
