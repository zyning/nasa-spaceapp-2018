import logging
import warnings

warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)


class DataQuester():
    """
    DataQuester to build seek and engineer features by quering DB
    """

    def __init__(self, db_connector):
        """
        Initialize the class with path to data file

        :param db_connector: DB connector to run queries
        :type  db_connector: :py:class:``
        """
        self.logger = logging.getLogger(__name__)
        self.db_connector = db_connector

    def join_incidents_to_tracts(self, export_to):
        """
        get tracts data
        
        :param export_to: 
        :type  export_to: :py:class:`str`

        DB Tables:
        - nyc_weather
        - nyc_tract
        - nyc_streets_segments
        - nyc_map_pluto_16v1
        - nyc_fire_incident
        - nyc_census
        """
        query = "update nyc_fire_incident set tract_id = ( select right_bloc from nyc_streets_segments where nyc_fire_incident.address = nyc_streets_segments.street)  where exists ( select right_bloc from nyc_streets_segments where nyc_fire_incident.address = nyc_streets_segments.street);"
        records = self.db_connector.run_query(query)
        return records

    def get_mappluto_data(self, export_to):
        """
        get mappluto data

        :param export_to: 
        :type  export_to: :py:class:`str`

        DB Tables:
        - nyc_map_pluto_16v1
        """
        query = "select bbl, tract2010, yearbuilt, comarea, resarea, officearea, retailarea, unitsres, bldgarea, assesstot, unitstotal, numbldgs, numfloors from nyc_map_pluto_16v1"
        records = self.db_connector.save_query_results(query, export_to)
        return records

    def get_buildings_data(self, export_to):
        """
        get buildings data

        :param export_to: 
        :type  export_to: :py:class:`str`
        
        DB Tables:
        - nyc_map_pluto_16v1
        """
        query = "select bbl, tract2010, yearbuilt, comarea, resarea, officearea, retailarea, unitsres, bldgarea, assesstot, unitstotal, numbldgs, numfloors from nyc_map_pluto_16v1"
        records = self.db_connector.save_query_results(query, export_to)
        return records
