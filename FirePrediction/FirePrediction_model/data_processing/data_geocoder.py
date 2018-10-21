# from data_acquisition.services.nominatim_client import NominatimAPI
# from data_acquisition.services.google_maps_client import GoogleMapsAPI
import pandas as pd
from math import isnan
import logging


class NYCGeocoder():

    def __init__(self, data=None, city="New York", state="NY", country="USA"):
        """

        :param data:
        :type data:

        :param city:
        :type city:

        :param state:
        :type state:

        :param country:
        :type country:

        """
        self.data = data

        self.city = city
        self.state = state
        self.country = country

    def convert_nyc_addr_to_latlng(self, fname_input, fname_out):
        """
        convert an address from New York City to Lat/Lng

        :param fname_input: the name of file to be converted
        :type fname_input: :py:class:`str`

        :param fname_out: the name of the output file
        :type fname_out: :py:class:`str`
        """
        df = pd.read_csv(fname_input)
        with open(fname_out, "w") as f_out:
            for index, row in df.iterrows():

                if isinstance(row[u'PROPERTY_USE_DESC'], str):
                    property_nbr = row[u'PROPERTY_USE_DESC'].split("-")[0].strip()

                    # UUU means undefined
                    if property_nbr == 'UUU':
                        property_nbr = ""
                elif isinstance(row[u'PROPERTY_USE_DESC'], float):
                    property_nbr = row[u'PROPERTY_USE_DESC']

                borough = row[u'BOROUGH_DESC'].split("-")[1].strip()

                # Cleaning the noises
                if isinstance(row[u'ZIP_CODE'], str):
                    zip_code = row[u'ZIP_CODE'].split("-")[0].strip

                elif isinstance(row[u'ZIP_CODE'], float) and isnan(row[u'ZIP_CODE']):
                    zip_code = ""

                else:
                    zip_code = int(row[u'ZIP_CODE'])

                street_highway = row[u'STREET_HIGHWAY']

                # convert address to: 2026 3rd Ave, New York, NY 10029, USA
                address = "{} {}, {}, {}, {} {}, {}".format(property_nbr, street_highway, borough, self.city,
                                                            self.state, zip_code, self.country)
                address_geo_info = geocoder_api.geocode(address)
                logging.info('Index: %s - Status: %s', index, address_geo_info.get(u'status'))
                if address_geo_info.get(u'status') == u'OK':
                    lat = address_geo_info.get('results', [])[0].get(u'geometry', {}).get(u'location', {}).get(u'lat',
                                                                                                               None)
                    lng = address_geo_info.get('results', [])[0].get(u'geometry', {}).get(u'location', {}).get(u'lng',
                                                                                                               None)
                    f_out.write("{}\t{}\t{}\n".format(index, lat, lng))
