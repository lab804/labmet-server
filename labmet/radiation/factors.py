#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from datetime import datetime


class Delta(object):
    """Delta

    The class is responsible to calculate the
    solar declination angle, in a given day of
    the year

    """

    def __init__(self, day):
        """Delta class init method

        Init method for the Delta class

        :param day: A given day datetime
        :type day: datetime
        """
        self.day = day

    @property
    def day(self):
        return self.__day

    @day.setter
    def day(self, day):
        if isinstance(day, datetime):
            self.__day = day.timetuple().tm_yday
        else:
            raise Exception("The day must be an datetime object!")

    def delta(self):
            """Delta

            The delta method calculates the delta itself.

            :return: the solar declination angle
            :rtype: float
            """
            return 23.45 * math.sin(math.radians(360.0 * (self.day - 81.0) / 365.0))


class RelativeSunEarthDistance(Delta):
    """Relative sun earth distance

    Calculates de relative distance between the sun and
    the earth(d/D), ie the ratio between the average
    distance between the earth and sun, and the distance of a
    given day

    """

    def relative_distance(self):
        """Relative Distance

        Calculates the relative distance.

        :return: relative sun earth distance
        :rtype: float
        """
        return 1.0 + 0.033 * math.cos(math.radians(self.day * 360.0 / 365.0))


class Photoperiod(RelativeSunEarthDistance):
    """Photoperiod

    Class to calculate the number of hour
    of a day in a given latitude

    """

    def __init__(self, day, lat):
        """Class init method

        Instantiate this class

        :param day: A given day datetime
        :param lat: int or float

        :type day: datetime
        :type lat: int or float
        """
        try:
            super(RelativeSunEarthDistance, self).__init__(day)
            self.lat = float(lat)
        except Exception as e:
            print("Erro: %s" % e)

    def _validate_latitude(self):
        """Validade latitude

        Validates the latitude interval

        :return: True if - 90 < latitude < 90
        :rtype: bool
        """
        if -90.0 <= self.lat <= 90.0:
            return True
        else:
            raise AttributeError("The latitude must be inside the interval +-90.0 ")

    def sunrise_time(self):
        """Sunrise time

        The time of the sunrise

        """
        if self._validate_latitude():
            return math.acos(-math.tan(math.radians(self.lat)) * math.tan(math.radians(self.delta()))) * 180.0 / math.pi

    def photoperiod(self):
        """Photoperiod

        Calculates a given day photoperiod

        """
        return 2.0 * self.sunrise_time() / 15.0
