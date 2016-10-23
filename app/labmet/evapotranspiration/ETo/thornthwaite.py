#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

from ...labmetExceptions import InputTypeException


class ThornthwaiteETo(object):
    """Thornthwaite ETo

    Empirical method based only on the mean air temperature,
    which is its main advantage. It was developed for wet
    weather conditions and therefore usually has underestimation
    of ETP in dry weather conditions. Despite this limitation, it
    is a method widely used for climatological purposes in
    monthly scales. This method is part of a standard ET (ETo),
    which is ET for a month of 30 days, with N = 12h.

    """

    def __init__(self, avg_temp, photoperiod, n_days,
                 avg_annual_temp):
        """Class init method

        Init method for the thornthwaite

        :param avg_temp: Period average air temperature
        :param photoperiod: Period average photoperiod
        :param n_days: Number of days
        :param avg_annual_temp: Average annual temperature

        :type avg_temp: int or float
        :type photoperiod: int or float
        :type n_days: int
        :type avg_annual_temp: int or float
        """
        try:
            self.avg_temp = float(avg_temp)
            self.photoperiod = float(photoperiod)
            self.n_days = self.period_validation(n_days)
            self.avg_annual_temp = float(avg_annual_temp)
        except Exception as e:
            print("Error: %s" % e)

        self.__temp_max_etp = 26.5

    @staticmethod
    def period_validation(n_days):
        """Period validation

        Static function to validate the maximum
        and minimum amount of days in a month

        :param n_days: The number of days

        :type n_days: int

        :return: The number of days, or raises Exception
        :rtype:int
        """
        if 1 <= int(n_days) <= 31:
            return n_days
        else:
            raise InputTypeException('The number of days in '
                                     'the period must be greater '
                                     'than 1 and lower than 31')

    def temp_eto_check(self):
        """Temperature ETo check

        method to determinate the type of ETo calculus

        :return: Bool flag to ETo calculus type
        :rtype: bool
        """
        if 0 <= self.avg_temp <= self.__temp_max_etp:
            return True
        else:
            return False

    def h_i(self):
        """Heat index

        Calculates an heat index which expresses
        the level of heat in a region

        :return: Heat index
        :type: float
        """
        return round(12 * math.pow((0.2 * self.avg_annual_temp), 1.514), 2)

    def a(self):
        """Thornthwaite ETo "a" exponent

        The "a" exponent is a regional thermal
        index and is calculated by a polynomial
        equation

        :return: "a" exponent
        :rtype: float
        """
        h_i = self.h_i()
        return round(0.49239 + (1.7912 * (math.pow(10, -2) * h_i))
                     - (7.71 * (math.pow(10, -5) * math.pow(h_i, 2)))
                     + (6.75 * (math.pow(10, -7) * math.pow(h_i, 3))), 2)

    def std_month_fix(self):
        """Standard month fix

        The ETo by definition is the monthly evapotranspiration
        in a standard month with 30 days and a photoperiod of
        12 hours. To get the value of the ETo of a corresponding
        month, it is necessary to fix it in function of the real
        number of days and photoperiod

        :return: Standard month fix factor
        :rtype: float
        """
        return round(self.photoperiod / 12.0 *
                     self.n_days / 30.0, 2)

    def eto(self):
        """Potential evapotranspiration

        This method is responsible to calculate
        the potential evapotranspiration by itself.

        :return: The ETo
        :rtype: float
        """
        i = self.h_i()
        a = self.a()
        if self.temp_eto_check():
            return round(16 * math.pow((10 * self.avg_temp / i), a), 2)
        else:
            return round(-415.85 + ((32.24 * self.avg_temp) -
                                    (0.43 * math.pow(self.avg_temp, 2))), 2)

    def eto_month(self):
        """Standard month ETo

        Calculates the ETo of a standard month,
        by multiplying the ETo with a standard
        month factor

        :return: The ETo of a given month
        :rtype: float
        """
        cor = self.std_month_fix()
        ETp = self.eto()
        return round(cor * ETp, 2)

    def eto_day(self):
        """ETo of a day

        Brings the ETo to a daily scale.

        :return: ETo of a given day
        :rtype: float
        """
        cor = self.std_month_fix()
        ETp = self.eto()
        return round((cor * ETp) / self.n_days, 2)

    def __str__(self):
        return "%.2f mm/month - %.2f mm/day" % (self.eto_month(), self.eto_day())


class ThornthwaiteCamargoETo(ThornthwaiteETo):
    """Thornthwaite Camargo method

    It's an adaptation of the thornthwaite method
    proposed by Camargo et al. and can be used in
    any climate condition. To use it's necessary to
    know the local thermal amplitude, instead of the average
    air temperature. The advantage is that the ETo is not
    underestimated in dry weather conditions. The downside is
    that there is now needed the max and min temperatures.
    As with the original Thornthwaite method, this method
    calculates a standard ET (ETo), which is ET for a month
    with 30 days, with N = 12h

    """

    def __init__(self, max_temp, min_temp, photoperiod, n_days,
                 avg_annual_temp):
        """Class init method

        The init method for the ThornthwaiteCamargoEto
        class.

        :param max_temp: The maximum temperature(ºC)
        :param min_temp: The minimum temperature(ºC)
        :param photoperiod: Period average photoperiod
        :param n_days: Number of days
        :param avg_annual_temp: Average annual temperature

        :type max_temp: int or float
        :type min_temp: int or float
        :type photoperiod: int or float
        :type n_days: int
        :type avg_annual_temp: int or float

        """
        try:
            self.tef = self.effective_temperature(max_temp, min_temp)
        except Exception as e:
            print("Error: %s" % e)

        ThornthwaiteETo.__init__(self, self.tef, photoperiod, n_days,
                                 avg_annual_temp)

    @staticmethod
    def effective_temperature(t_max, t_min):
        """Effective temperature

        Calculus of the effective temperature

        :param t_max: The maximum temperature
        :param t_min: The minimum temperature

        :type t_max: int or float
        :type t_min: int or float

        :return: Effective temperature
        :rtype: float
        """
        if t_max < t_min:
            t_max, t_min = t_min, t_max

        return round(0.36 * (3 * t_max - t_min), 2)


if __name__ == '__main__':
    test = ThornthwaiteETo(24.4, 13.4, 31, 21.1)
    print("Thornthwaite: \t\t", test)
    test2 = ThornthwaiteCamargoETo(13, 10, 10.6, 31, 21.1)
    print("Thornthwaite Camargo: \t", test2)
