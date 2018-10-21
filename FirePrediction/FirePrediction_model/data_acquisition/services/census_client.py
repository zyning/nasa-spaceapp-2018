import requests
import logging
import json

# Handle library reorganisation Python 2 > Python 3.
try:
    from urllib.parse import urljoin
    from urllib.parse import urlencode
except ImportError:
    from urlparse import urljoin
    from urllib import urlencode


class CensusAPIClient():
    BASE_URL = "http://api.census.gov/data"
    SPATIAL_UNITS = {'zipc': '&for=zip+code+tabulation+area:*', 'zipcode': '&for=zipcode:*',
                     'county': '&for=county:*&in=state:*', 'all': '&for=block:*&tract:*&in=state:*&county:*'}

    def __init__(self, year, data_id, var_list, table_id, spatial_unit, key):
        """
        clean & normalize address string

        :param year: the year
        :type year: :py:class:`str`

        :param data_id: the id of the data to fetch
        :type data_id: :py:class:`str`

        :param var_list: variables
        :type var_list: :py:class:`list`

        :param table_id: the id of the table
        :type table_id: :py:class:`str`

        :param spatial_unit: the spatial unit (ex: zipc, zipcode, county, state)
        :type spatial_unit: :py:class:`str`

        :param key: the key to fetch the api
        :type key: :py:class:`str`

        :param str_addr: street name
        :type str_addr: :py:class:`str`
        """
        self.year = year
        self.key = key
        self.data_id = data_id
        self.table_id = table_id
        self.var_list = ",".join(['NAME'] + var_list)
        self.spatial_unit = spatial_unit

        self.var_url = "{}/{}/{}/variables.json".format(self.BASE_URL, self.year, self.data_id)
        self.api_url = "{}/{}/{}?get={}{}&key={}".format(self.BASE_URL, self.year, self.data_id, self.var_list,
                                                         self.SPATIAL_UNITS[self.spatial_unit], key)

    def _get(self, url):
        """
        Handle GET requests

        :param str_addr: street name
        :type str_addr: :py:class:`str`
        """

        try:
            response = requests.get(url)

            print response.status_code
            if response.status_code == requests.codes.ok:
                return response
            else:
                return None

        except requests.exceptions.RequestException as e:
            print e
            return None

    def get_variable_info(self):
        """
        get the information on the variable

        :param str_addr: street name
        :type str_addr: :py:class:`str`
        """
        respose = self._get(self.var_url)

        return respose.json()

    def get_all_census_data(self, fname):
        """
        get the census data, & store the data into a file with name 'fname'

        :param fname: street name
        :type fname: :py:class:`str`
        """
        logging.info('API Url: %s', self.api_url)

        respose = self._get(self.api_url)
        with open(fname, "w") as f:
            f.write(respose.text.encode('utf-8'))
        f.close()

    def get_census_data(self, spatial_unit, fname):
        """
        get the census data filtered by a spatial unit, & store the data into file with name 'fname'

        :param fname: street name
        :type fname: :py:class:`str`

        spatial units: Nation, Regions, Divisions, State, County, Census Tract, Block Group, Census Block

        """

        if spatial_unit['granularity'] == 'county':
            spatial_unit = "&for=county:{}&in=state:{}".format(spatial_unit['county'], spatial_unit['state'])

        elif spatial_unit['granularity'] == 'blockgroup':
            # spatial_unit = "&for=block+group:{}&in=state:{}+county:{}+tract:{}".format(spatial_unit['blockgroup'],  spatial_unit['state'] , spatial_unit['county'] ,spatial_unit['tract'] )
            spatial_unit = "&for=block+group:{}&in=state:{}".format(spatial_unit['blockgroup'], spatial_unit['state'])

        elif spatial_unit['granularity'] == 'tract':
            # spatial_unit = "&for=block+group:{}&in=state:{}+county:{}+tract:{}".format(spatial_unit['blockgroup'],  spatial_unit['state'] , spatial_unit['county'] ,spatial_unit['tract'] )

            spatial_unit = "&for=tract:{}&in=state:{}".format(spatial_unit['tract'], spatial_unit['state'])

        api_url = "{}/{}/{}?get={}{}&key={}".format(self.BASE_URL, self.year, self.data_id, self.var_list, spatial_unit,
                                                    self.key)

        # #  requests information on the 2015 ACS's occupations characteristics variables from the Census Bureau
        logging.info('Fetching data from : %s', api_url)

        respose = self._get(api_url)

        with open(fname, "w") as f:
            for line in json.loads(respose.text):
                f.write("\t".join(map(lambda x: x if x is not None else "", line)) + "\n")
        f.close()

        return respose
