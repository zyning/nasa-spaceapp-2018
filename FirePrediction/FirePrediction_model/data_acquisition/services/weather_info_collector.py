import requests
import logging
import json
from datetime import datetime, timedelta
import pandas as pd

# Handle library reorganisation Python 2 > Python 3.
try:
    from urllib.parse import urljoin
    from urllib.parse import urlencode
except ImportError:
    from urlparse import urljoin
    from urllib import urlencode
from data_acquisition.services.wunderground_client import WundergroundAPI
from ast import literal_eval


class WeatherInfoCollector():

    def __init__(self, start_date, end_date):
        """
        initialize the class with start/ending date

        :param start_date: the starting date
        :type start_date: :py:class:`str`

        :param end_date: the end date
        :type end_date: :py:class:`str`
        """
        self.start_date = start_date
        self.end_date = end_date

    @staticmethod
    def generate_dates(start_date, end_date):
        """
        generate a list of dates between start_date and end_date

        :param start_date: the starting date
        :type start_date: :py:class:`str`

        :param end_date: the end date
        :type end_date: :py:class:`str`

        """
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        for n in range(int((end_date - start_date).days)):
            yield (start_date + timedelta(n)).strftime('%Y%m%d')

    def filter_dailysummary_data(self, json_obj):
        """
        filter data based on the

        :param json_obj: dict that holds weather info
        :type json_obj: :py:class:`dict`

        """

        columns = ['mintempm', 'maxtempm', 'humidity', 'snow', 'snowfallm', 'snowdepthm', 'meanpressurem',
                   'meanwindspdm', 'precipm', 'rain']
        _ = {col: json_obj[col] for col in columns}
        _['date'] = "{}-{}-{}".format(json_obj[u'date'][u'mday'], json_obj[u'date'][u'mon'], json_obj[u'date'][u'year'])
        return _

    def filter_weather_data(self, input_fname, output_fname):
        """
        filter weather data file

        :param input_fname: the name of the output file
        :type input_fname: :py:class:`str`

        :param output_fname: the name of the output file
        :type output_fname: :py:class:`str`
        """

        data = []
        with open(input_fname) as f:
            for line in f:
                dt, json_data = line.rstrip("\n").split("\t")
                data += [self.filter_dailysummary_data(literal_eval(json_data))]

        columns = ['observation_date_time', 'mintempm', 'maxtempm', 'humidity', 'snow', 'snowdepthm', 'meanpressurem',
                   'meanwindspdm', 'precipm', 'rain']
        df = pd.DataFrame(data)

        # precipm sometimes has 'T' for trace amounts of rain. Replace this with epsilon
        epsilon = 0.001
        df['precipm'] = df['precipm'].replace('T', epsilon)
        df['snowdepthm'] = df['snowdepthm'].replace('T', epsilon)
        df['observation_date_time'] = df['date']

        df.to_csv(output_fname, columns=columns, index=False, sep="\t")

    def get_weather_info_period(self, wunderground_keys_fname, output_fname, region="NY", city="New_York"):
        """
        initialize the class with start/ending date


        :param wunderground_keys_fname: the file name that holds wunderground keys
        :type wunderground_keys_fname: :py:class:`str`

        :param output_fname: the name of the output file
        :type output_fname: :py:class:`str`

        :param region: the name of the region
        :type region: :py:class:`str`

        :param city: the name of the city 
        :type city: :py:class:`str`
        """
        wunderground_api = WundergroundAPI(wunderground_keys_fname)
        with open(output_fname, "w") as f:

            for dt in self.generate_dates(self.start_date, self.end_date):
                try:
                    logging.info('Getting weather data for date: %s.', dt)
                    data = wunderground_api.get_hest_daily_weather_info(dt, region=region, city=city)
                    daily_summary_data = data.get('history', {}).get('dailysummary', {})[0]
                    f.write("{}\t{}\n".format(dt, str(daily_summary_data)))

                except Exception as e:
                    wunderground_api.cur_key = wunderground_api.keys.next()
                    wunderground_api.set_auth()
