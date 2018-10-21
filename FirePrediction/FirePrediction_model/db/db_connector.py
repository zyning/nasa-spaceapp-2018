import psycopg2
import psycopg2.extras
import logging


class DBConnector:

    def __init__(self, db_config):
        """
        :param db_config: config file for the db
        :type db_config: :py:class:`dict`

        db_config = {
            "host": <value>,
            "port": <value>,
            "db_name": <value>, 
            "user": <value>,
            "password": <value>, 
            }
        """

        self.connection_str = "host = '{0}' dbname = '{1}' user = '{2}' password = '{3}'".format(db_config["host"],
                                                                                                 db_config["database"],
                                                                                                 db_config["user"],
                                                                                                 db_config["password"])
        self.connection = None

    def connect(self):
        """
        connect to database
        """
        try:
            self.connection = psycopg2.connect(self.connection_str)
            # self.connection = psycopg2.connect(host= db_config["host"],port= db_config["port"],database= db_config["database"],user= db_config["user"],password= db_config["user"])
        except:
            logging.warn("Unable to connect to the server")

    def run_query(self, query):
        """
        connect to database and run the query

        :param query: query to be run against the DB
        :type query: :py:class:`str`
        """

        with psycopg2.connect(self.connection_str) as self.connection:
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)  as cursor:
                cursor.execute(query)
                return cursor.fetchall()

    def save_query_results(self, query, export_to):
        """
        connect to database, run the query and store results

        :param query: query to be run against the DB
        :type query: :py:class:`str`
        """
        with psycopg2.connect(self.connection_str) as self.connection:
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)  as cursor:
                outputquery = "COPY ({0}) TO STDOUT WITH CSV DELIMITER '\t' HEADER".format(query)
                with open(export_to, 'w') as f:
                    cursor.copy_expert(outputquery, f)
