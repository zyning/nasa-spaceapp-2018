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

from itertools import cycle


class WundergroundAPI():
    BASE_URL = "http://api.wunderground.com/api/"

    def __init__(self, wunderground_keys_fname):
        """
        initialize the class with start/ending date

        :param wunderground_keys_fname: the file name that holds wunderground keys
        :type wunderground_keys_fname: :py:class:`str`
        """

        self.json_tokens = json.loads(open(wunderground_keys_fname).read())
        self.base_url = self.BASE_URL
        self.keys = cycle(self.json_tokens.keys())
        self.cur_key = self.keys.next()
        self.set_auth()

    def set_auth(self):
        """
        authentication setter

        """
        key = self.json_tokens[self.cur_key].get("wunderground_api_key")
        self.base_url = "http://api.wunderground.com/api/{}".format(key)

        logging.info('\n Switched to another key %s', self.cur_key)

    def _get(self, url):
        """
        Handle GET requests

        :param url: the url to parse data
        :type url: :py:class:`str`
        """
        # url = "{}{}".format(url_endpoint)

        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            return response
        else:
            return None

    def get_hest_daily_weather_info(self, dt, region, city):
        """
        get the historical daily weather information

        :param dt: the date to collect weather data
        :type dt: :py:class:`str`

        :param region: the name of the region
        :type region: :py:class:`str`

        :param city: the name of the city 
        :type city: :py:class:`str`
        """

        loc_endpoint = "/q/{}/{}.json".format(region, city)
        time_endpoint = "/history_{}".format(dt)

        url_endpoint = "{}{}{}".format(self.base_url, time_endpoint, loc_endpoint)

        respose = self._get(url_endpoint)

        return respose.json()

    def get_daily_forecast(self, region, city):
        """
        get daily forecasts in specific region

        :param dt: the date to collect weather data
        :type dt: :py:class:`str`

        :param region: the name of the region
        :type region: :py:class:`str`

        :param city: the name of the city 
        :type city: :py:class:`str`
        """

        loc_endpoint = "/q/{}/{}.json".format(region, city)
        time_endpoint = "/forecast"
        url_endpoint = "{}{}{}".format(self.base_url, time_endpoint, loc_endpoint)
        respose = self._get(url_endpoint)
        return respose.json()
