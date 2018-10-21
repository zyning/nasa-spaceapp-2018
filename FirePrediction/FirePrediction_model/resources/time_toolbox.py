from datetime import datetime, timedelta
import logging


class TimeToolbox():
    def __init__(self, date_format=None):
        self.date_format = date_format

    def normalize_dt(self, from_dt, from_dt_format, to_dt_format):
        """
        convert a date from a dateformat to another

        :param from_dt: date time in `datetime` format
        :type  from_dt: :py:class:`obj`

        :param from_dt_format: date format to be converted from
        :type  from_dt_format: :py:class:`obj`

        :param to_dt_format: date format to be converted to
        :type  to_dt_format: :py:class:`obj`

        :return: DateTime 
        """
        try:
            if isinstance(from_dt, str):
                from_dt = self.convert_to_datetime(from_dt, from_dt_format)
            return self.convert_to_str(from_dt, to_dt_format)
        except Exception as e:
            logging.info('Error! Datetime is not valid')
            return None

    def get_weekday(self, dt, dt_format, litteral=0):
        """
        get weekday form datetime dt

        :param dt: date time in `datetime` format
        :type  dt: `datetime`
        
        :param dt_format: date format
        :type  dt_format: `datetime`

        :return: index of weekday
        """
        if isinstance(dt, str):
            dt = self.convert_to_datetime(dt, dt_format)

        if litteral == 0:
            return dt.weekday()
        else:
            return dt.strftime("%A")

    def get_month(self, dt, dt_format):
        """
        get month from datetime dt

        :param dt: date time in `datetime` format
        :type  dt: :py:class:`str`

        :param dt_format: date format
        :type  dt_format: :py:class:`obj`

        :return: index of weekday
        """
        if isinstance(dt, str):
            dt = self.convert_to_datetime(dt, dt_format)
        else:
            dt = dt

        return dt.month

    def get_year(self, dt_str):
        """
        get year from datetime dt

        :param dt_str: date object to be converted
        :type  dt_str: :py:class:`obj`

        :return: index of weekday
        """
        if isinstance(dt_str, str):
            dt = self.convert_to_datetime(dt_str)
        else:
            dt = dt_str

        return dt.year

    def get_hour(self, dt_str):
        """
        convert a string to datetime

        :param dt_str: date object to be converted
        :type  dt_str: :py:class:`obj`

        :return: DateTime 
        """
        if isinstance(dt_str, str):
            dt = self.convert_to_datetime(dt_str)
        else:
            dt = dt_str

        return dt.hour

    def get_minute(self, dt_str):
        """
        convert a string to datetime

        :param dt_str: date object to be converted
        :type  dt_str: :py:class:`obj`

        :return: DateTime 
        """
        if isinstance(dt_str, str):
            dt = self.convert_to_datetime(dt_str)
        else:
            dt = dt_str

        return dt.minutes

    def get_seconds(self, dt_str):
        """
        convert a string to datetime

        :param dt_str: date object to be converted
        :type  dt_str: :py:class:`obj`

        :return: DateTime 
        """
        if isinstance(dt_str, str):
            dt = self.convert_to_datetime(dt_str)
        else:
            dt = dt_str

        return dt.seconds

    @staticmethod
    def convert_to_datetime(dt_str, date_format):
        """
        convert a string to datetime

        :param dt_str: date time in `str` format
        :type  dt_str: :py:class:`str`

        :param date_format: date format
        :type  date_format: ``

        :return: DateTime 
        """

        return datetime.strptime(dt_str, date_format)

    def convert_to_str(self, dt, date_format):
        """
        convert a datetime to string 

        :param dt: date time in `datetime` format
        :type  dt: `datetime`

        :param date_format: date format
        :type  date_format: ``

        :return: string format for DateTime 
        """

        return dt.strftime(date_format)

    def find_diff_days(self, dt_a, dt_b, date_format):
        """
        find number of days between two dates dt_a, dt_b

        :param dt_a: date time in `datetime` format
        :type  dt_a: :py:class:`obj`

        :param dt_b: date time in `datetime` format
        :type  dt_b: :py:class:`obj`

        :param date_format: date format
        :type  date_format: ``

        :return: number of days
        """

        return (self.convert_to_datetime(dt_a, date_format) - self.convert_to_datetime(dt_b, date_format)).days

    def generate_dates(self, from_dt, to_dt, date_format, to_dt_format):
        """
        generate dates from/to time

        :param from_dt: date time in `datetime` format
        :type  from_dt: `datetime`

        :param to_dt: date time in `datetime` format
        :type  to_dt: `datetime`

        :param date_format: date format
        :type  date_format: ``

        :param to_dt_format: to date format
        :type  to_dt_format: ``

        :return: string format for DateTime 
        """
        DAYS, HOURS, MINUTES, SECONDS = 3600 * 24, 3600, 60, 1

        if isinstance(from_dt, str):
            from_dt = self.convert_to_datetime(from_dt, date_format)

        if isinstance(to_dt, str):
            to_dt = self.convert_to_datetime(to_dt, date_format)

        # calculate the difference between times
        elapsed_time = (to_dt - from_dt).total_seconds()

        # calculate the number of hours 
        nbr_days = divmod(elapsed_time, DAYS)[0]

        # generate datetimes -> range of dates
        dates_range = [from_dt + timedelta(days=x) for x in range(0, int(nbr_days))]

        # convert datetime -> range of dates
        dates_range = map(lambda dt: self.convert_to_str(dt, to_dt_format), dates_range)

        return dates_range
