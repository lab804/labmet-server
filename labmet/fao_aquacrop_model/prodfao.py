#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..labmetExceptions import InputException, InputTypeException

__author__ = 'joaotrevizoliesteves, Murilo Ijanc'
__copyright__ = "Copyright 2015, Lab804"
__license__ = "BSD"
__version__ = "0.1"


class PotentialProductivity(object):
    """Raw Crop potential estimate

    Method for estimating the standard Raw potential productivity,
    based on the Doorembos & Kassan (1994) ie AquaCrop model (FAO 33, 1994)

    :param ho: Average Extraterrestrial irradiation energy
     on a plane horizontal(MJ⁻² . day⁻1)
    :param n: Averge Insulation (hours)
    :param N: Average Photoperiod (hours)
    :param temp_cloudy_days_fix: Correction for cloudy days
     in function of the Temperature (dimensionless)
    :param temp_clear_days_fix: Correction for clear days
     in function of the Temperature (dimensionless)

    :type ho: int or float
    :type n: int or float
    :type N: int or float
    :type temp_cloudy_days_fix: int or float
    :type temp_clear_days_fix: int or float

    """

    def __init__(self, ho, temp_cloudy_days_fix, temp_clear_days_fix, n=None, N=None, n_N=None):
        try:
            self.ho = float(ho)
            self.temp_cloudy_days_fix = float(temp_cloudy_days_fix)
            self.temp_clear_days_fix = float(temp_clear_days_fix)
        except:
            raise InputTypeException("The ho, temp_cloudy_fix and temp_clear_days_fix "
                                     "must be castable to float!")

        self.n = n
        self.N = N
        self.n_N = n_N

        if (n or N) is None and n_N is None :
            raise InputException("It's required to enter the insulation(n) "
                                 "and the photoperiod(N) or its relation(n_N)!")

    @property
    def n_N(self):
        return self.__n_N

    @n_N.setter
    def n_N(self, n_N):
        if n_N is not None:
            self.__n_N = n_N
        elif self.n is not None and self.N is not None:
            self.__n_N = self.n / self.N
        else:
            raise InputException("It's required to the n/N relation or to "
                                 "use the n and N as inputs.")

    def raw_potential_productivity_cloudy_days(self, ho_cloudy=None, hectometer_sqr_m=True):
        """Potential Productivity for cloudy days

        Calculates de potential productivity for cloudy days.

        :param ho_cloudy: Average Extraterrestrial irradiation energy
        on a plane horizontal for cloudy days(MJ⁻² . day⁻1)
        :param hectometer_sqr_m: The potential productivity unity to be return,
        if True the unity is kilograms/squared hectometer meters (kg/hm²)
        if false kilogram / squared meters (kg/m²), default=True

        :type ho_cloudy: int or float
        :type hectometer_sqr_m: bool


        :return: The raw potential productivity for cloudy days (kg/hm² or kg/m²)
        :rtype: float
        """

        if ho_cloudy is None:
            ho_cloudy = self.ho

        cloudy_pot_prod = (
            (31.7 + 0.219 * ho_cloudy) *
            self.temp_cloudy_days_fix * (1 - self.n_N)
        )

        if hectometer_sqr_m:
            return cloudy_pot_prod
        else:
            return cloudy_pot_prod / 10000

    def raw_potential_productivity_clear_days(self, ho_clear=None, hectometer_sqr_m=True):
        """Potential Productivity for clear days

        Calculates de potential productivity for clear days.

        :param ho_clear: Average Extraterrestrial irradiation energy
        on a plane horizontal for clear days(MJ⁻² . day⁻1)
        :param hectometer_sqr_m: The potential productivity unity to be return,
        if True the unity is kilograms/squared hectometer meters (kg/hm²)
        if false kilogram / squared meters (kg/m²), default=True

        :type ho_clear: int or float
        :type hectometer_sqr_m: bool


        :return: The raw potential productivity for clear days (kg/hm² or kg/m²)
        :rtype: float
        """

        if ho_clear is None:
            ho_clear = self.ho

        clear_pot_prod = (
            (107.2 + 0.36 * ho_clear) *
            self.temp_clear_days_fix * (self.n_N)
        )

        if hectometer_sqr_m:
            return clear_pot_prod
        else:
            return clear_pot_prod / 10000

    def raw_potential_productivity(self,n_cycle_days=1, ho_cloudy=None, ho_clear=None, hectometer_sqr_m=True):
        """Raw Potential Productivity

        Calculates de raw potential productivity of the given period,
        it is the sum of the potential productivity for clear days and
        the potential productivity for cloudy days.

        :return:
        """
        if ho_cloudy is None:
            ho_cloudy = self.ho
        if ho_clear is None:
            ho_clear = self.ho

        cloudy_productivity = self.raw_potential_productivity_cloudy_days(ho_cloudy, hectometer_sqr_m)
        clear_productivity = self.raw_potential_productivity_clear_days(ho_clear, hectometer_sqr_m)

        return (
            (cloudy_productivity + clear_productivity) * n_cycle_days
        )

    def potential_productivity(self, leaf_area_fix, breathing_fix,
                               harvested_part_fix, n_cycle_days=1,
                               ho_cloudy=None, ho_clear=None,
                               hectometer_sqr_m=True):
        """Potential Productivity

        Calculates the potential productivity of a given period/culture,
        it is the potential productive pondered with fixes for the leaf area,
        breathing, harvested part and number of days in the plant cycle

        :param leaf_area_fix: The fix for the plant leaf area (dimensionless)
        :param breathing_fix: The fix for the plant breathing (dimensionless)
        :param harvested_part_fix: The fix for the plant harvested part (dimensionless)
        :param n_cycle_days: The number of days contained in the cycle
        :param ho_cloudy: Average Extraterrestrial irradiation energy
        on a plane horizontal for cloudy days(MJ⁻² . day⁻1)
        :param ho_clear: Average Extraterrestrial irradiation energy
        on a plane horizontal for clear days(MJ⁻² . day⁻1)
        :param hectometer_sqr_m: The potential productivity unity to be return,
        if True the unity is kilograms/squared hectometer meters (kg/hm²)
        if false kilogram / squared meters (kg/m²), default=True

        :type leaf_area_fix: int or float
        :type breathing_fix: int or float
        :type harvested_part_fix: int or float
        :type n_cycle_days: int
        :type ho_cloudy: int or float
        :type ho_clear: int or float
        :type hectometer_sqr_m: bool

        :return: The potential productivity(kg/hm² or kg/m²)
        :rtype: float
        """

        raw_pot_productivity = self.raw_potential_productivity(n_cycle_days, ho_cloudy,
                                                               ho_clear, hectometer_sqr_m)

        pot_productivity = (
            raw_pot_productivity *
            leaf_area_fix *
            breathing_fix *
            harvested_part_fix
        )

        return pot_productivity

    def __str__(self, ho_cloudy=None, ho_clear=None, hectometer_sqr_m=True):
        str_rpr = "Raw potential productivity on cloudy days: {:.3f} {},\n" \
               "Raw potential productivity on clear days: {:.3f} {},\n" \
               "Raw potential productivity: {:.2f} {}"

        if hectometer_sqr_m:
            unit = "Kg/hm²"
        else:
            unit = "Kg/m²"

        cloudy_productivity = self.raw_potential_productivity_cloudy_days(ho_cloudy, hectometer_sqr_m)
        clear_productivity = self.raw_potential_productivity_clear_days(ho_clear, hectometer_sqr_m)
        pot_productivity = self.raw_potential_productivity(ho_cloudy, ho_clear, hectometer_sqr_m)

        return str_rpr \
            .format(cloudy_productivity, unit,
                    clear_productivity, unit,
                    pot_productivity, unit)


class ObtainableProductivity(object):
    def __init__(self, ky):
        self.ky = ky

    def obtainable_productivity(self, eto, etc, potential_productivity):
        return (1 - self.ky * (1 - eto / etc)) * potential_productivity
