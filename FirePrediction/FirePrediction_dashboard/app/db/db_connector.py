import psycopg2
import psycopg2.extras
import logging
import sys
import pprint
import yaml
import os

class MongoDBConnector:

    def __init__(self,config_src):
        self.db_config = yaml.load(open("{}/{}".format(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','config')),config_src )))    
        self.connection_str = "host = '{0}' dbname = '{1}' user = '{2}' password = '{3}'".format(self.db_config["host"],self.db_config["database"], self.db_config["user"],self.db_config["password"])
        self.connect()


    def __del__(self):
        self.connection.close()

    def to_dicts(self,records):
        return map(lambda row: dict(records), records)


    def connect(self):
        try:
            self.connection = psycopg2.connect(self.connection_str)
            #self.connection = psycopg2.connect(host= db_config["host"],port= db_config["port"],database= db_config["database"],user= db_config["user"],password= db_config["user"])
        except:
            logging.warn("Unable to connect to the server")


    def run_query(self, query):
        with psycopg2.connect(self.connection_str) as self.connection:
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)  as cursor:
                cursor.execute(query)
                return  cursor.fetchall()

