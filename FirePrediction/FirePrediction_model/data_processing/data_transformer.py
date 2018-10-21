import pandas as pd
import json
from math import isnan
from collections import Counter, defaultdict
import re
from shapely.wkt import loads
import logging
import geopandas as gpd
from resources.constants import RELEVANT_FEATURES, STANDARD_TIME_FORMAT, VIOLATION_FORMAT, COMPLAINT_FORMAT, \
    STANDARD_TIME_FORMAT_M, BORO_STR_CODE, BORO_CODE, CENSUS_FIELDS, INCIDENT_TIME_FORMAT, DAY_TIME_FORMAT, NULL, \
    STANDARD_TIME_FORMAT
from resources.time_toolbox import TimeToolbox
import numpy as np


class DataTransformer():

    def __init__(self, data=None):
        self.data = data

    def normalize_address(self, street_address):
        """
        clean & normalize address string

        :param street_address: street name
        :type street_address: :py:class:`str`
        """

        if isinstance(street_address, float) and isnan(street_address):
            street_address = NULL
        else:
            street_address = " ".join(
                [self.ordinal(piece) if piece.isdigit() else str(piece).rstrip() for piece in street_address.split()])
        return street_address.upper()

    def json_to_csv(self, input_fname, out_fname):
        """
        convert the json file to csv

        :param input_fname: the name of file to be converted
        :type input_fname: :py:class:`str`

        :param out_fname: the name of the output file
        :type out_fname: :py:class:`str`
        """
        data = json.load(open(input_fname))
        columns = [x.get('name') for x in data.get('meta', {}).get('view', {}).get("columns")]
        _ = []
        for i, line in enumerate(data[u'data']):
            _ += [{x: y for x, y in zip(columns, line)}]

        pd.DataFrame(_).to_csv(out_fname, columns=columns, index=False, sep="\t")

    @staticmethod
    def ordinal(nbr):
        """
        Returns i + the ordinal indicator for the number.

        :param nbr: street name
        :type nbr: :py:class:`str`

        Example: ordinal(3) => '3rd'
        """
        nbr = int(nbr)

        if nbr % 100 in (11, 12, 13):
            return '%sth' % nbr

        ORD_INDICATOR = 'th'
        _ = nbr % 10
        if _ == 1:
            ORD_INDICATOR = 'st'
        elif _ == 2:
            ORD_INDICATOR = 'nd'
        elif _ == 3:
            ORD_INDICATOR = 'rd'

        return '%s%s' % (nbr, ORD_INDICATOR)

    def normalize_nyc_incidents_file(self, input_fname, out_fname):
        """
        clean & normalize data of the file

        :param input_fname: the name of file to be converted
        :type input_fname: :py:class:`str`

        :param out_fname: the name of the output file
        :type out_fname: :py:class:`str`
        """
        df = pd.read_csv(input_fname, sep=",", dtype=str)

        logging.info("DataFrame has been loaded")

        df[u'ZIP_CODE'].apply(lambda x: x.split("-")[0].strip if isinstance(x, str) else str(x))

        df[u'BOROUGH_DESC'] = df[u'BOROUGH_DESC'].apply(lambda x: x.split('-', 1)[1]).str.replace('Manhattan',
                                                                                                  'New York')
        df[u'BOROUGH_DESC'] = df[u'BOROUGH_DESC'].str.replace('Brooklyn', 'Kings')
        df[u'BOROUGH_DESC'] = df[u'BOROUGH_DESC'].str.replace('Staten Island', 'RICHMOND')

        df[u'BOROUGH_DESC'] = df[u'BOROUGH_DESC'].apply(
            lambda x: NULL if isinstance(x, float) and isnan(x) else x.upper())
        df[u'ZIP_CODE'] = df[u'ZIP_CODE'].apply(lambda x: NULL if isinstance(x, float) and isnan(x) else x.upper())
        # 'W 151st ST, NEW YORK, NY 10031'
        df[u'ADDRESS'] = df.apply(
            lambda x: "{},{}, NY {}".format(self.normalize_address(x['STREET_HIGHWAY']), x['BOROUGH_DESC'],
                                            x['ZIP_CODE']), axis=1)

        df.rename(columns={_: _.lower().replace(" ", "_") for _ in df.columns}, inplace=True)

        # print df[u'ADDRESS'].values()
        df.to_csv(out_fname, index=False, sep="\t")

    def join_with_tracts(self, incidents_input_fname, street_input_fname, output_fname):
        """
        join two files input_fname, out_fname

        https://www.policymap.com/2012/08/tips-on-fips-a-quick-guide-to-geographic-place-codes-part-iii/

        :param incidents_input_fname: the name of file that contains incidents input
        :type incidents_input_fname: :py:class:`str`

        :param street_input_fname: the name of file that contains streets information
        :type street_input_fname: :py:class:`str`

        :param output_fname: the name of the output file
        :type output_fname: :py:class:`str`
        """
        FIPS_CODE_NBR = 11

        df_streets = pd.read_csv(street_input_fname, sep="\t")
        df_incidents = pd.read_csv(incidents_input_fname, sep="\t")

        # map streets to tracts
        streets_tracts_mapper = {x: str(y)[:FIPS_CODE_NBR] for (x, y) in
                                 zip(df_streets[u'street'].values, df_streets[u'left_block'].values)}

        # I avoided using string similarity to infer streets' names. However, we can use text matching with a threshold
        df_incidents[u'census_tract'] = df_incidents[u'address'].apply(lambda x: streets_tracts_mapper.get(x, None))

        # filter those that are not in the street dataset
        df_incidents = df_incidents[df_incidents[u'census_tract'] != None]

        # mark relevant columns
        relevant_columns = ['incident_date_time', 'address', 'census_tract']

        # export to csv file
        df_incidents[relevant_columns].to_csv(output_fname, index=False, sep="\t")

    def flatten_incidents_tracts(self, incidents_input_fname, nyc_census_fname, output_fname):
        """
        flatten incidents/

        :param incidents_input_fname: the name of file that contains incidents input
        :type incidents_input_fname: :py:class:`str`

        :param nyc_census_fname: the name of file that contains census tracts information
        :type nyc_census_fname: :py:class:`str`

        :param output_fname: the name of the output file
        :type output_fname: :py:class:`str`
        """
        time_toolbox = TimeToolbox()

        # load csv files
        df_incidents = pd.read_csv(incidents_input_fname, sep="\t", dtype=str)
        df_nyc_census = pd.read_csv(nyc_census_fname, sep="\t", dtype=str)

        # get the min/max of datetime + get all possible dates
        min_dt_time, max_dt_time = min(df_incidents['incident_date_time'].values), max(
            df_incidents['incident_date_time'].values)
        all_possible_dates = time_toolbox.generate_dates(min_dt_time, max_dt_time, INCIDENT_TIME_FORMAT,
                                                         STANDARD_TIME_FORMAT)

        # # normalize census tract field
        df_nyc_census[u'census_tract'] = df_nyc_census.apply(
            lambda x: "{}{}{}".format(x['state'], str(x['county']).zfill(3), str(x['tract']).zfill(6)), axis=1)
        all_possible_tracts = df_nyc_census[u'census_tract'].values

        # # # group-by incidents datetime to calculate the frequency
        df_incidents[u'incident_date_time'] = df_incidents['incident_date_time'].apply(
            lambda dt: time_toolbox.normalize_dt(dt, INCIDENT_TIME_FORMAT, STANDARD_TIME_FORMAT))
        df_incidents = df_incidents.groupby([u'incident_date_time', u'census_tract']).size().reset_index(
            name='nbr_incidents')

        # augment data
        incidents_mapper = {(dt, tract): 0 for dt in all_possible_dates for tract in all_possible_tracts}

        for row_index, row in df_incidents.iterrows():
            incidents_mapper[(row[u'incident_date_time'], row[u'census_tract'])] = row[u'nbr_incidents']

        with open(output_fname, "w") as f:
            f.write("{}\t{}\t{}\n".format(u'incident_date_time', u'census_tract', u'nbr_incidents'))
            for dt in all_possible_dates:
                for tract in all_possible_tracts:
                    nbr_incidents = incidents_mapper[(dt, tract)]
                    f.write("{}\t{}\t{}\n".format(dt, tract, nbr_incidents))

    def join_with_census_data(self, incidents_tracts_fname, nyc_census_fname, out_fname):
        """
        join two files incidents_tracts_fname, nyc_census_fname >> incidents_tracts_census_fname

        :param incidents_input_fname: the name of file that contains incidents/tracts input
        :type incidents_input_fname: :py:class:`str`

        :param nyc_census_fname: the name of file that contains contextual data nyc_census_fname
        :type nyc_census_fname: :py:class:`str`

        :param out_fname: the name of the output file
        :type out_fname: :py:class:`str`
        """

        # logging.info("DataFrame has been loaded")

        df_incidents_tracts = pd.read_csv(incidents_tracts_fname, sep="\t", dtype=str)
        df_nyc_census = pd.read_csv(nyc_census_fname, sep="\t", dtype=str)

        df_nyc_census[u'census_tract'] = df_nyc_census.apply(
            lambda x: "{}{}{}".format(x['state'], str(x['county']).zfill(3), str(x['tract']).zfill(6)), axis=1)

        df = pd.merge(df_incidents_tracts, df_nyc_census, on='census_tract')

        df.to_csv(out_fname, index=False, sep="\t")

    def rename_columns(self, input_fname):
        """
        rename the columns, from encoded to readable columns

        :param input_fname: the name of file that contains incidents/tracts input
        :type input_fname: :py:class:`str`
        """
        # load file
        df = pd.read_csv(input_fname, sep="\t", dtype=str)
        # remame census
        df.rename(columns={_: CENSUS_FIELDS.get(_, _) for _ in df.columns}, inplace=True)
        # convert to csv file
        df.to_csv(input_fname, index=False, sep="\t")

    def join_with_weather_data(self, incidents_tracts_census_fname, weather_fname, out_fname):
        """
        join two files incidents_tracts_census, weather_fname >> incidents_tracts_census_weather_fname

        :param incidents_tracts_census_fname: the name of file that contains incidents/tracts input
        :type incidents_tracts_census_fname: :py:class:`str`

        :param weather_fname: the name of file that contains weather's information on a daily basis
        :type weather_fname: :py:class:`str`

        :param out_fname: the name of the output file
        :type out_fname: :py:class:`str`
        """
        df_incidents_tracts_census = pd.read_csv(incidents_tracts_census_fname, sep="\t", dtype=str)
        df_weather = pd.read_csv(weather_fname, sep="\t", dtype=str)

        df = pd.merge(df_incidents_tracts_census, df_weather, left_on='incident_date_time',
                      right_on='observation_date_time')

        # convert to csv file
        df.to_csv(out_fname, index=False, sep="\t")

    def join_complains_tracts(self, db_complaints_fname, street_input_fname, out_fname):
        """
        join two files

        :param db_complaints_fname:
        :type db_complaints_fname: :py:class:`str`

        :param street_input_fname:
        :type street_input_fname: :py:class:`str`

        :param out_fname: the name of the output file
        :type out_fname: :py:class:`str`
        """

        return None

    def aggregate_complaints_data(self, bin_bbl_fname, dob_complaints_fname, dob_complaints_agg_fname):
        """
        aggregate dob file

        :param bin_bbl_fname: file name
        :type bin_bbl_fname :py:class:`str

        :param dob_complaints_fname: file name
        :type dob_complaints_fname: :py:class:`str`

        :param dob_complaints_agg_fname:file name
        :type dob_complaints_agg_fname: :py:class:`str`

        references: 
        - https://www1.nyc.gov/assets/buildings/pdf/complaint_category.pdf
        """
        time_toolbox = TimeToolbox()

        # lambda functions to process the data
        pad_zeros = lambda x: '0' * (len(x) - 5) + x
        remove_zeros = lambda x: x[1:] if len(x) == 5 else x
        standarize_boro = lambda x: x[:1] if len(x) > 1 else x

        # new york bin/bbl buildings
        df_bin_bbl = pd.read_csv(bin_bbl_fname, sep="\t", dtype=str)

        # reading csv file
        df_dob_complaints = pd.read_csv(dob_complaints_fname, sep=",", dtype=str)

        # add BIN
        df_dob_complaints = df_dob_complaints.merge(df_bin_bbl, how='inner', on='BIN')

        # convert time to monthly
        df_dob_complaints[u'Date Entered'] = df_dob_complaints[u'Date Entered'].apply(
            lambda dt: time_toolbox.normalize_dt(dt, COMPLAINT_FORMAT, STANDARD_TIME_FORMAT_M))

        df_dob_complaints = df_dob_complaints[[u'census_tract', u'Date Entered', u'Disposition Code']]

        # total complaints/disposition monthly
        # no need to filter specific dispositions/ complaints
        df_temp_a = df_dob_complaints[[u'census_tract', u'Date Entered', u'Disposition Code']].groupby(
            [u'census_tract', u'Date Entered', u'Disposition Code']).size().reset_index(name='nbr_dispositions')
        df_temp_b = df_dob_complaints[[u'census_tract', u'Date Entered', u'Complaint Category']].groupby(
            [u'census_tract', u'Date Entered', u'Complaint Category']).size().reset_index(name='nbr_complaints')

        df = pd.merge(df_temp_a, df_temp_b, on=[u'census_tract', u'Date Entered'])

        df[[u'census_tract', u'Date Entered', 'nbr_dispositions', 'nbr_complaints', ]].to_csv(dob_complaints_agg_fname,
                                                                                              index=False, sep="\t")

    def aggregate_violations_data(self, bin_bbl_fname, dob_violations_fname, ecb_violations_fname,
                                  dob_ecb_violations_agg_fname):
        """
        aggregate violations file

        :param bin_bbl_fname: file name
        :type bin_bbl_fname :py:class:`str

        :param dob_violations_fname: file name
        :type dob_violations_fname: :py:class:`str`

        :param ecb_violations_fname: file name
        :type ecb_violations_fname: :py:class:`str`

        :param dob_ecb_violations_agg_fname:file name
        :type dob_ecb_violations_agg_fname: :py:class:`str`
        """
        time_toolbox = TimeToolbox()

        # lambda functions to process the data
        pad_zeros = lambda x: '0' * (len(x) - 5) + x
        remove_zeros = lambda x: x[1:] if len(x) == 5 else x
        standarize_boro = lambda x: x[:1] if len(x) > 1 else x
        pad_year = lambda x: '20' + x.replace(" ", "") if len(x.replace(" ", "")) == 6 else x

        # new york bin/bbl buildings
        df_bin_bbl = pd.read_csv(bin_bbl_fname, sep="\t", dtype=str)

        # read csv files
        df_ecb_violations = pd.read_csv(ecb_violations_fname, sep=",", dtype=str)
        df_dob_violations = pd.read_csv(dob_violations_fname, sep=",", dtype=str)

        # # clean / merge df_dob_violations
        df_ecb_violations[u'BORO'] = df_ecb_violations[u'BORO'].astype(str)
        df_ecb_violations[u'BLOCK'] = df_ecb_violations[u'BLOCK'].astype(str)
        df_ecb_violations[u'LOT'] = df_ecb_violations[u'LOT'].astype(str)
        df_ecb_violations[u'BBL'] = df_ecb_violations.apply(
            lambda row: "{}{}{}".format(standarize_boro(row[u'BORO']), pad_zeros(row[u'BLOCK']),
                                        remove_zeros(row[u'LOT'])), axis=1)

        # filter relevant columns
        df_ecb_violations = df_ecb_violations[[u'BBL', 'ISSUE_DATE', 'VIOLATION_TYPE']]

        # add BIN
        df_ecb_violations = df_ecb_violations.merge(df_bin_bbl, how='inner', on='BBL')

        # filter data
        df_ecb_violations[u'_remove'] = df_ecb_violations[u'ISSUE_DATE'].apply(lambda x: len(x) == 8)
        df_ecb_violations = df_ecb_violations[df_ecb_violations[u'_remove'] == True]

        # # convert time to monthly
        df_ecb_violations[u'ISSUE_DATE'] = df_ecb_violations[u'ISSUE_DATE'].apply(
            lambda dt: time_toolbox.normalize_dt(pad_year(dt), VIOLATION_FORMAT, STANDARD_TIME_FORMAT_M))

        # total ecb/dob violations monthly
        # no need to filter specific dispositions/ complaints
        df_temp_a = df_ecb_violations[[u'census_tract', u'ISSUE_DATE']].groupby(
            [u'census_tract', u'ISSUE_DATE']).size().reset_index(name='nbr_ecb_violations')

        # new york bin/bbl buildings
        df_bin_bbl = pd.read_csv(bin_bbl_fname, sep="\t", dtype=str)

        # clean / merge df_ecb_violations
        df_dob_violations[u'BORO'] = df_dob_violations[u'BORO'].astype(str)
        df_dob_violations[u'BLOCK'] = df_dob_violations[u'BLOCK'].astype(str)
        df_dob_violations[u'LOT'] = df_dob_violations[u'LOT'].astype(str)
        df_dob_violations[u'DISPOSITION_DATE'] = df_dob_violations[u'DISPOSITION_DATE'].astype(str)
        df_dob_violations[u'BBL'] = df_dob_violations.apply(
            lambda row: "{}{}{}".format(row[u'BORO'], pad_zeros(row[u'BLOCK']), remove_zeros(row[u'LOT'])), axis=1)

        # add BIN
        df_dob_violations = df_dob_violations.merge(df_bin_bbl, how='inner', on='BBL')

        # filter data
        df_dob_violations[u'_remove'] = df_dob_violations[u'ISSUE_DATE'].apply(lambda x: len(x) == 8)
        df_dob_violations = df_dob_violations[df_dob_violations[u'_remove'] == True]

        # convert time to month
        df_dob_violations[u'ISSUE_DATE'] = df_dob_violations[u'ISSUE_DATE'].apply(
            lambda dt: time_toolbox.normalize_dt(pad_year(dt), VIOLATION_FORMAT, STANDARD_TIME_FORMAT_M))
        df_dob_violations = df_dob_violations[df_dob_violations[u'ISSUE_DATE'] != None]

        # total ecb/dob violations monthly
        # no need to filter specific dispositions/ complaints
        df_temp_b = df_dob_violations[[u'census_tract', u'ISSUE_DATE']].groupby(
            [u'census_tract', u'ISSUE_DATE']).size().reset_index(name='nbr_dob_violations')

        # merge df_temp_a/df_temp_b on outer and export the file
        df = pd.merge(df_temp_a, df_temp_b, how='outer', on=[u'census_tract', u'ISSUE_DATE'])
        df.to_csv(dob_ecb_violations_agg_fname, index=False, sep="\t")

    def aggregate_permits_data(self, bin_bbl_fname, dob_permits_fname, dob_permits_agg_fname):
        """
        aggregate permits

        :param bin_bbl_fname: file name
        :type bin_bbl_fname :py:class:`str

        :param dob_permits_fname: file name
        :type dob_permits_fname: :py:class:`str`

        :param dob_permits_agg_fname:file name
        :type dob_permits_agg_fname: :py:class:`str`
        """
        time_toolbox = TimeToolbox()

        # lambda functions to process the data
        pad_zeros = lambda x: '0' * (len(x) - 5) + x
        remove_zeros = lambda x: x[1:] if len(x) == 5 else x
        standarize_boro = lambda x: x[:1] if len(x) > 1 else x
        pad_year = lambda x: '20' + x.replace(" ", "") if len(x.replace(" ", "")) == 6 else x

        # new york bin/bbl buildings
        df_bin_bbl = pd.read_csv(bin_bbl_fname, sep="\t", dtype=str)

        df_dob_permits = pd.read_csv(dob_permits_fname, sep=",", dtype=str)

        # # clean / merge df_ecb_violations
        df_dob_permits[u'BOROUGH'] = df_dob_permits[u'BOROUGH'].astype(str)
        df_dob_permits[u'Block'] = df_dob_permits[u'Block'].astype(str)
        df_dob_permits[u'Lot'] = df_dob_permits[u'Lot'].astype(str)
        df_dob_permits[u'BBL'] = df_dob_permits.apply(
            lambda row: "{}{}{}".format(BORO_STR_CODE[row[u'BOROUGH']], pad_zeros(row[u'Block']),
                                        remove_zeros(row[u'Lot'])), axis=1)

        # add BIN
        df_dob_permits = df_dob_permits.merge(df_bin_bbl, how='inner', on=u'BBL')
        df_dob_permits['Issuance Date'] = df_dob_permits['Issuance Date'].apply(
            lambda dt: time_toolbox.normalize_dt(dt, INCIDENT_TIME_FORMAT, STANDARD_TIME_FORMAT_M))
        df_dob_permits = df_dob_permits[df_dob_permits['Issuance Date'] != None]
        df = df_dob_permits[[u'census_tract', 'Issuance Date']].groupby(
            [u'census_tract', 'Issuance Date']).size().reset_index(name='nbr_dob_permits')
        df.to_csv(dob_permits_agg_fname, index=False, sep="\t")

    def aggregate_mappluto(self, mappluto_fname, mappluto_agg_fname):
        """
        aggregate mappluto file

        :param mappluto_fname: the name of mappluto file to be processed
        :type mappluto_fname: :py:class:`str`

        :param mappluto_agg_fname: the name of the aggregated mappluto file
        :type mappluto_agg_fname: :py:class:`str`
        """

        # reading csv file
        df = pd.read_csv(mappluto_fname, sep="\t", dtype=str)
        df['bbl'] = df['bbl'].apply(lambda x: x.split(".")[0])
        df['census_tract'] = df[['bbl', 'tract2010']].apply(
            lambda x: "{}{}00".format(BORO_CODE[x['bbl'][:1]], x['tract2010']) if len(
                x['tract2010']) == 4 else "{}{}".format(BORO_CODE[x['bbl'][:1]], x['tract2010']), axis=1)

        # buildings' age
        df[u'yearbuilt'] = df[u'yearbuilt'].astype(float)

        # building area
        df[u'bldgarea'] = df[u'bldgarea'].astype(float)

        # total number of residential units
        df[u'unitsres'] = df[u'unitsres'].astype(float)

        # The sum of residential and non-residential
        df[u'unitstotal'] = df[u'unitstotal'].astype(float)

        # building use
        df[u'resarea'] = df[u'resarea'].astype(float)
        df[u'officearea'] = df[u'officearea'].astype(float)
        df[u'retailarea'] = df[u'retailarea'].astype(float)
        df[u'comarea'] = df[u'comarea'].astype(float)

        # The number of buildings on the tax lot.
        df[u'numbldgs'] = df[u'numbldgs'].astype(float)

        # In the tallest building on the tax lot, the number of full and partial stories starting from the ground floor.
        df[u'numfloors'] = df[u'numfloors'].astype(float)

        df_tracts = pd.DataFrame(list(set(df[u'census_tract'].values)), columns=['census_tract'])

        # calculate The average number of floors for every census tract
        df_numfloors = df[[u'census_tract', u'numfloors']].groupby([u'census_tract'], as_index=False).mean()
        df_numfloors = df_numfloors.rename(columns={'numfloors': 'avg_numfloors'})

        # calculate the average building age for every census tract
        df_yearbuilt = df[[u'census_tract', u'yearbuilt']].groupby([u'census_tract'], as_index=False).mean()
        df_yearbuilt = df_yearbuilt.rename(columns={'yearbuilt': 'avg_yearbuilt'})

        # calculate Total units for every census tract
        df_unitstotal = df[[u'census_tract', u'unitstotal']].groupby([u'census_tract'], as_index=False).sum()
        df_unitstotal = df_unitstotal.rename(columns={'unitstotal': 'total_units'})

        # calculate the average Unit area for every census tract
        df_bldgarea = df[[u'census_tract', u'bldgarea']].groupby([u'census_tract'], as_index=False).mean()
        df_unitarea = pd.merge(df_unitstotal, df_bldgarea, on='census_tract')
        df_unitarea['avg_unitarea'] = df_unitarea.apply(
            lambda row: 0 if float(row[u'total_units']) == 0 else row[u'bldgarea'] / float(row[u'total_units']), axis=1)

        # calculate building area
        df_bldgarea = df[[u'census_tract', u'bldgarea']].groupby([u'census_tract'], as_index=False).sum()
        df_bldgarea = df_bldgarea.rename(columns={'bldgarea': 'total_bldgarea'})

        # res / total units by tract  bldgarea/unitstotal
        df_ratio_unitarea = pd.merge(df_unitstotal, df_bldgarea, on='census_tract')
        df_ratio_unitarea['ratio_unitarea'] = df_ratio_unitarea.apply(
            lambda row: 0 if float(row[u'total_units']) == 0 else row[u'total_bldgarea'] / float(row[u'total_units']),
            axis=1)

        # commercial ratio by tract comarea/bldgarea
        df_comarea = df[[u'census_tract', u'comarea']].groupby([u'census_tract'], as_index=False).sum()
        df_ratio_com = pd.merge(df_comarea, df_bldgarea, on='census_tract')
        df_ratio_com['ratio_comarea'] = df_ratio_com.apply(
            lambda row: 0 if float(row[u'total_bldgarea']) == 0 else row[u'comarea'] / float(row[u'total_bldgarea']),
            axis=1)

        # residential ratio by tract resarea/bldgarea
        df_resarea = df[[u'census_tract', u'resarea']].groupby([u'census_tract'], as_index=False).sum()
        df_ratio_resarea = pd.merge(df_resarea, df_bldgarea, on='census_tract')
        df_ratio_resarea['ratio_resarea'] = df_ratio_resarea.apply(
            lambda row: 0 if float(row[u'total_bldgarea']) == 0 else row[u'resarea'] / float(row[u'total_bldgarea']),
            axis=1)

        # office ratio by tract officearea/bldgarea
        df_officerea = df[[u'census_tract', u'officearea']].groupby([u'census_tract'], as_index=False).sum()
        df_ratio_officerea = pd.merge(df_officerea, df_bldgarea, on='census_tract')
        df_ratio_officerea['ratio_officerea'] = df_ratio_officerea.apply(
            lambda row: 0 if float(row[u'total_bldgarea']) == 0 else row[u'officearea'] / float(row[u'total_bldgarea']),
            axis=1)

        # retail ratio by tract retailarea/bldgarea
        df_retailarea = df[[u'census_tract', u'retailarea']].groupby([u'census_tract'], as_index=False).sum()
        df_ratio_retailarea = pd.merge(df_retailarea, df_bldgarea, on='census_tract')
        df_ratio_retailarea['ratio_retailarea'] = df_ratio_retailarea.apply(
            lambda row: 0 if float(row[u'total_bldgarea']) == 0 else row[u'retailarea'] / float(row[u'total_bldgarea']),
            axis=1)

        # mean unit area by tract unitsres/unitstotal
        df_resunits = df[[u'census_tract', u'unitsres']].groupby([u'census_tract'], as_index=False).sum()
        df_avg_resunits = pd.merge(df_resunits, df_unitstotal, on='census_tract')
        df_avg_resunits['avg_unitsres'] = df_avg_resunits.apply(
            lambda row: 0 if float(row[u'total_units']) == 0 else row[u'unitsres'] / float(row[u'total_units']), axis=1)

        # merge data-frames and export CSV files
        data_frames = [df_tracts, df_avg_resunits, df_ratio_retailarea, df_ratio_officerea, df_ratio_resarea,
                       df_ratio_com, df_numfloors, df_yearbuilt, df_unitstotal, df_unitarea, df_bldgarea]
        df_mappluto_agg = reduce(lambda left, right: pd.merge(left, right, on=['census_tract'], how='inner'),
                                 data_frames)

        relevant_columns = [u'census_tract', u'avg_unitsres', u'ratio_retailarea', u'ratio_resarea', u'ratio_comarea',
                            u'avg_yearbuilt', u'ratio_officerea', u'avg_numfloors', u'total_units', u'avg_unitarea',
                            u'total_bldgarea']

        # convert to csv file
        df_mappluto_agg[relevant_columns].to_csv(mappluto_agg_fname, index=False, sep="\t")

    def normalize_street_file(self, input_fname, out_fname):
        """
        clean & normalize street file

        :param input_fname: the name of file to be converted
        :type input_fname: :py:class:`str`

        :param out_fname: the name of the output file
        :type out_fname: :py:class:`str`
        """
        df = pd.read_csv(input_fname, sep=",", dtype=str)

        # logging.info("DataFrame has been loaded")
        NYC_COUNTIES = ['Queens', 'New York', 'Richmond', 'Bronx', 'Kings']

        relevant_columns = ['LEFT_STREET', 'RIGHT_STREET', u'WKT']

        # filter columns here in NYC
        # df = df[relevant_columns]

        # filter roads in nYC
        df[u'LEFT_STREET'] = df.apply(
            lambda x: "{}, {}, NY {}".format(str(x['Label']).upper(), str(x['LeftCounty']).upper(),
                                             str(x['LeftPostal']).upper()), axis=1)
        df[u'RIGHT_STREET'] = df.apply(
            lambda x: "{}, {}, NY {}".format(str(x['Label']).upper(), str(x['RightCount']).upper(),
                                             str(x['RightPosta']).upper()), axis=1)

        # crs = {'init': 'epsg:4326'}
        nyc_streets = defaultdict(set)
        nyc_streets_blocks = defaultdict(dict)

        # Query right streets
        for index, row in df.iterrows():
            # index street -> census_id for both right/left blocks
            nyc_streets_blocks[row['RIGHT_STREET']]['right'] = row[u'RightCensu']
            nyc_streets_blocks[row['RIGHT_STREET']]['left'] = row[u'LeftCensus']

            # index street -> geom
            nyc_streets[row['RIGHT_STREET']].add(row[u'WKT'])

        # Query left streets
        for index, row in df.iterrows():
            # index street -> census_id for both right/left blocks
            nyc_streets_blocks[row['LEFT_STREET']]['right'] = row[u'RightCensu']
            nyc_streets_blocks[row['LEFT_STREET']]['left'] = row[u'LeftCensus']

            # index street -> geom
            nyc_streets[row['LEFT_STREET']].add(row[u'WKT'])

        # build a csv to get releavant information on street/geometry
        street_gp = gpd.GeoDataFrame(columns=['street', 'geometry', 'right_block', 'left_block'], crs='EPSG:4326')

        # iterate your dictionary
        n = len(nyc_streets.items())
        for i, (street_name, street_geo) in enumerate(nyc_streets.items()):
            geometry = gpd.GeoSeries(map(lambda x: loads(x), list(street_geo)))
            geometry = geometry.unary_union
            # geometry = cascaded_union(map(lambda x: loads(x) , list(street_geo)))
            street_gp.set_value(i, 'street', street_name)
            street_gp.set_value(i, 'right_block', nyc_streets_blocks[street_name]['right'])
            street_gp.set_value(i, 'left_block', nyc_streets_blocks[street_name]['left'])
            street_gp.set_value(i, 'geometry', geometry)

        street_gp.to_file(out_fname, driver="ESRI Shapefile")

    def join_with_complaints_data(self, incidents_context_fname, complaints_fname, out_fname):
        """
        join two files complaints, with contextual data

        :param incidents_context_fname: the name of file that contains incidents/tracts input
        :type incidents_context_fname: :py:class:`str`

        :param complaints_fname:
        :type complaints_fname: :py:class:`str`

        :param out_fname: the name of the output file
        :type out_fname: :py:class:`str`
        """
        df_incidents_context = pd.read_csv(incidents_context_fname, sep="\t", dtype=str)
        df_dob_complaints = pd.read_csv(complaints_fname, sep="\t", dtype=str)
        df_dob_complaints.rename(columns={u'Date Entered': u'incident_date_time'}, inplace=True)

        df_incidents_context = pd.merge(df_incidents_context, df_dob_complaints,
                                        on=['census_tract', 'incident_date_time'], how='left')
        # convert to csv file
        df_incidents_context.to_csv(out_fname, index=False, sep="\t")

    def join_with_violations_data(self, incidents_context_fname, violations_fname, out_fname):
        """
        join two files complaints, with contextual data

        :param incidents_context_fname: the name of file that contains incidents/tracts input
        :type incidents_context_fname: :py:class:`str`

        :param violations_fname:
        :type violations_fname: :py:class:`str`

        :param out_fname: the name of the output file
        :type out_fname: :py:class:`str`
        """
        df_incidents_context = pd.read_csv(incidents_context_fname, sep="\t", dtype=str)
        df_dob_violations = pd.read_csv(violations_fname, sep="\t", dtype=str)

        df_dob_violations.rename(columns={u'ISSUE_DATE': u'incident_date_time'}, inplace=True)
        df_incidents_context = pd.merge(df_incidents_context, df_dob_violations,
                                        on=['census_tract', 'incident_date_time'], how='left')
        # convert to csv file
        df_incidents_context.to_csv(out_fname, index=False, sep="\t")

    def join_with_permits_data(self, incidents_context_fname, permits_fname, out_fname):
        """
        join two files complaints, with contextual data

        :param incidents_context_fname: the name of file that contains incidents/tracts input
        :type incidents_context_fname: :py:class:`str`

        :param permits_fname:
        :type permits_fname: :py:class:`str`

        :param out_fname: the name of the output file
        :type out_fname: :py:class:`str`
        """
        df_incidents_context = pd.read_csv(incidents_context_fname, sep="\t", dtype=str)
        df_permits = pd.read_csv(permits_fname, sep="\t", dtype=str)
        df_permits.rename(columns={u'Issuance Date': u'incident_date_time'}, inplace=True)
        df_incidents_context = pd.merge(df_incidents_context, df_permits, on=['census_tract', 'incident_date_time'],
                                        how='left')
        # convert to csv file
        df_incidents_context.to_csv(out_fname, index=False, sep="\t")

    def join_with_mappluto_data(self, incidents_context_fname, mappluto_agg_fname, out_fname):
        """
        join two files complaints, with contextual data

        :param incidents_context_fname: the name of file that contains incidents/tracts input
        :type incidents_context_fname: :py:class:`str`

        :param mappluto_agg_fname:
        :type mappluto_agg_fname: :py:class:`str`

        :param out_fname: the name of the output file
        :type out_fname: :py:class:`str`
        """
        df_incidents_context = pd.read_csv(incidents_context_fname, sep="\t", dtype=str)
        df_mappluto_agg = pd.read_csv(mappluto_agg_fname, sep="\t", dtype=str)
        df_mappluto_agg = df_mappluto_agg.rename(columns={u'Issuance Date': u'incident_date_time'})
        df_incidents_context = pd.merge(df_incidents_context, df_mappluto_agg, on=['census_tract'], how='left')
        df_incidents_context.to_csv(out_fname, index=False, sep="\t")

    def encode_time_features(self, incidents_context_fname):
        """
        encode time features

        :param incidents_context_fname: the name of file that contains incidents/tracts input
        :type incidents_context_fname: :py:class:`str`
        """
        time_toolbox = TimeToolbox()

        df_incidents_context = pd.read_csv(incidents_context_fname, sep="\t", dtype=str)

        df_incidents_context['week_day'] = df_incidents_context['incident_date_time'].apply(
            lambda dt: time_toolbox.get_weekday(dt, STANDARD_TIME_FORMAT))
        df_incidents_context['month'] = df_incidents_context['incident_date_time'].apply(
            lambda dt: time_toolbox.get_month(dt, STANDARD_TIME_FORMAT))

        # One-hot encoding on time-dependent categorical feartures
        # weekdays
        df_incidents_context['wday_mon'] = df_incidents_context['week_day'].apply(lambda dt: 1 if dt == 0 else 0)
        df_incidents_context['wday_tue'] = df_incidents_context['week_day'].apply(lambda dt: 1 if dt == 1 else 0)
        df_incidents_context['wday_wed'] = df_incidents_context['week_day'].apply(lambda dt: 1 if dt == 2 else 0)
        df_incidents_context['wday_thu'] = df_incidents_context['week_day'].apply(lambda dt: 1 if dt == 3 else 0)
        df_incidents_context['wday_fri'] = df_incidents_context['week_day'].apply(lambda dt: 1 if dt == 4 else 0)
        df_incidents_context['wday_sat'] = df_incidents_context['week_day'].apply(lambda dt: 1 if dt == 5 else 0)
        df_incidents_context['wday_sun'] = df_incidents_context['week_day'].apply(lambda dt: 1 if dt == 6 else 0)

        # months
        df_incidents_context['month_jan'] = df_incidents_context['month'].apply(lambda dt: 1 if dt == 1 else 0)
        df_incidents_context['month_feb'] = df_incidents_context['month'].apply(lambda dt: 1 if dt == 2 else 0)
        df_incidents_context['month_mar'] = df_incidents_context['month'].apply(lambda dt: 1 if dt == 3 else 0)
        df_incidents_context['month_apr'] = df_incidents_context['month'].apply(lambda dt: 1 if dt == 4 else 0)
        df_incidents_context['month_may'] = df_incidents_context['month'].apply(lambda dt: 1 if dt == 5 else 0)
        df_incidents_context['month_jun'] = df_incidents_context['month'].apply(lambda dt: 1 if dt == 6 else 0)
        df_incidents_context['month_jul'] = df_incidents_context['month'].apply(lambda dt: 1 if dt == 7 else 0)
        df_incidents_context['month_aug'] = df_incidents_context['month'].apply(lambda dt: 1 if dt == 8 else 0)
        df_incidents_context['month_sep'] = df_incidents_context['month'].apply(lambda dt: 1 if dt == 9 else 0)
        df_incidents_context['month_oct'] = df_incidents_context['month'].apply(lambda dt: 1 if dt == 10 else 0)
        df_incidents_context['month_nov'] = df_incidents_context['month'].apply(lambda dt: 1 if dt == 11 else 0)
        df_incidents_context['month_dec'] = df_incidents_context['month'].apply(lambda dt: 1 if dt == 12 else 0)

        # convert to csv file
        df_incidents_context.to_csv(incidents_context_fname, index=False, sep="\t")

    def filter_relevant_features(self, incidents_context_fname, incidents_context_final_fname):
        """
        join two files complaints, with contextual data

        :param incidents_context_fname: the file name of
        :type incidents_context_fname: :py:class:`str`

        :param incidents_context_final_fname: the file name of
        :type incidents_context_final_fname: :py:class:`str`

        """
        df_incidents_context = pd.read_csv(incidents_context_fname, sep="\t", dtype=str)

        df_incidents_context = df_incidents_context[RELEVANT_FEATURES]
        df_incidents_context = df_incidents_context.replace(np.nan, 0)
        # convert to csv file
        df_incidents_context.to_csv(incidents_context_final_fname, columns=RELEVANT_FEATURES, index=False, sep="\t")
