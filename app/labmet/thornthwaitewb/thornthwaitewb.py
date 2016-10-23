#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Thornthwaite water balance calculus

Copyright 2016, Lab804

.. module: labmet.base.thornthwaitewb.thornthwaitewb
   :platform: Unix, Windows, macOS
   :synopsis: All the procedures used to compute the
    Thornthwaite water balance.

.. moduleauthor:: João Trevizoli Esteves <joao@lab804.com.br>
"""

import math

from math import exp, log
from base.labmetExceptions import InputException

__author__ = 'joaotrevizoliesteves, Murilo Ijanc'
__copyright__ = "Copyright 2015, Lab804"
__license__ = "BSD"
__version__ = "0.1"


class ThornthwaiteWaterBalance(object):
    """Thornthwaite Water Balance

    This class is used to compute the Thornthwaite
    water balance. The Thornthwaite water balance uses
    an accounting procedure  to analyze the allocation of
    water among various components of the hydrologic system.

    .. warning::
        To use this class it's necessary to instantiate it and call the
        thornthwaite_water_balance method at least once
         or use the classmethod thornthwaite_wb_simple

    """
    def __init__(self, awc, soil_water_moisture=0,
                 accumulated_negative=None, variation=None,
                 potential_et=None, real_et=None,
                 deficit=None, excess=None):
        """
        Thorthwaite Water Balance class initialization

        .. note::
            Remember to call the thornthwaite_water_balance method at least
            once when it's required to update all the initial kwargs

        :param awc: The awc is the available water
         content in millimeters(mm)
        :param soil_water_moisture: The initial soil
         water moisture in millimeters(mm), default = 0
        :param accumulated_negative: The initial accumulated
         negative in millimeters(mm), optional
        :param variation: The initial variation in millimeters(mm),
         optional
        :param potential_et: The initial potential evapotranspiration,
         optional
        :param real_et: The initial real evapotranpiration,
         optional
        :param deficit: The initial deficit, optional
        :param excess: The initial excess

        :type awc: int or float
        :type soil_water_moisture: int or float
        :type accumulated_negative: int, float or None
        :type variation: int, float or None
        :type potential_et: int, float or None
        :type deficit: int, float or None
        :type excess: int, float or None

        """
        try:
            self.awc = float(awc)
            self.soil_water_moisture = float(soil_water_moisture)

            self.accumulated_negative = accumulated_negative
            self.variation = variation
            self.potential_et = potential_et
            self.real_et = real_et
            self.deficit = deficit
            self.excess = excess

            self._pet_precipitation = None
            self.__precipitation = None
            self.__pet = None
            self.__init_soil_water_moisture = self.soil_water_moisture
        except Exception as e:
            print("Error: %s" % e)

    def __check_pet_precipitation(self):
        """ PET minus precipitation check

        Private method to check if the potential evapotranspiration minus
         the precipitation are greater than zero

        :return: A true boolean if the result is greater than zero
        :rtype: bool
        """
        if self._pet_precipitation >= 0:
            return True
        else:
            return False

    def __update_accumulated_negative(self):
        """Updates the accumulated negative value

        Private method to update the value of the
         accumulated negative

        """
        check_etp_p = self.__check_pet_precipitation()
        if self.accumulated_negative is None:
            if check_etp_p:
                self.accumulated_negative = 0
            else:
                self.accumulated_negative = self._pet_precipitation
        else:
            if check_etp_p:
                self.__updated_soil_water_moisture()
                self.accumulated_negative = \
                    self.awc * log(self.soil_water_moisture/self.awc)
            else:
                self.accumulated_negative = - abs(self.accumulated_negative) \
                                            + self.__precipitation - self.__pet

    def __updated_soil_water_moisture(self):
        """Updates the soil water moisture value

        Private method to updated the value of
        the soil water moisture

        """
        if self.__check_pet_precipitation():
            soil_water_moisture = self.__init_soil_water_moisture + \
                                  self.__precipitation - self.__pet
            if soil_water_moisture > self.awc:
                self.soil_water_moisture = self.awc
            else:
                self.soil_water_moisture = soil_water_moisture
        else:
            self.soil_water_moisture = \
                self.awc * exp(-abs(self.accumulated_negative/self.awc))

    def __update_variation(self):
        """Uptades the variation value

        Private method to update the soil
         water variation value in the period

        """
        if self.variation is None:
            if self.__check_pet_precipitation():
                self.variation = 0
            else:
                self.variation = self.soil_water_moisture - self.awc
        else:
            self.variation = \
                self.soil_water_moisture - self.__init_soil_water_moisture

        self.__init_soil_water_moisture = self.soil_water_moisture

    def __update_real_et(self):
        """Updates the real evapotranspiration value

        Private method to update the real
         evapotranspiration value

        """
        if self.__check_pet_precipitation():
            self.real_et = self.__pet
        else:
            self.real_et = self.__precipitation + abs(self.variation)

    def __update_deficit(self):
        """Updates the deficits value

        Private method to update the
         deficit value

        """
        if self.__check_pet_precipitation():
            self.deficit = 0
        else:
            self.deficit = self.__pet - self.real_et

    def __update_excess(self):
        """Updates the excess value

        Private method to update the
         excess value

        """
        if self.soil_water_moisture < self.awc:
            self.excess = 0
        else:
            self.excess = self._pet_precipitation - self.variation

    def thornthwaite_water_balance(self, precipitation=None, pet=None):
        """Thornthwaite water balance

        This is main method of this class. This method updates
        all the water balance variables by calling all the
        private methods in the correct order

        .. note::
            To update the water balance with new values its required to pass
            precipitation and pet values to this method, but if just a  report
            is required and its not necessary to update the water balance
            just call this methods with the default args

        .. warning::
            It is required to call this method at least once
            with precipitation and pet values

        :param precipitation: The precipitation in the period.
        :param pet: The potential evapotranspiration in the period

        :type precipitation: int or float
        :type pet: int or float

        :return: A dict with a report
        with all the water balance values
        :rtype: dict
        """
        if precipitation and pet is not None:
            self.__precipitation = precipitation
            self.__pet = pet
            self._pet_precipitation = self.__precipitation - self.__pet
            self.__update_accumulated_negative()
            self.__updated_soil_water_moisture()
            self.__update_variation()
            self.__update_real_et()
            self.__update_deficit()
            self.__update_excess()

        elif self.__precipitation is None or self.__pet is None:
                raise InputException("You must enter the precipitation and the"
                                     " pet at least once in the object life")
        return {
            "precipitation_pet": self._pet_precipitation,
            "soil_water_moisture": self.soil_water_moisture,
            "accumulated_negative": self.accumulated_negative,
            "variation": self.variation,
            "real_et": self.real_et,
            "pet": self.__pet,
            "deficit": self.deficit,
            "excess": self.excess,
            "precipitation": self.__precipitation
        }

    @classmethod
    def thornthwaite_wb_simple(cls, cad, precipitation, pet):
        """S

        :param cad:
        :param precipitation:
        :param pet:
        :return:
        """
        thornthwaite_wb_simple = cls(cad)
        thornthwaite_wb_simple.thornthwaite_water_balance(precipitation, pet)
        return thornthwaite_wb_simple


if __name__ == '__main__':

    data = {
        "awc": 100,
    }
    t_wb_data = {"pet": 25,
                 "precipitation": 10}
    t_wb = ThornthwaiteWaterBalance(**data)
    print(t_wb.thornthwaite_water_balance(**t_wb_data))

    t_wb_data = {"pet": 25,
                 "precipitation": 100}
    print(t_wb.thornthwaite_water_balance(**t_wb_data))

    t_wb_data = {"pet": 45,
                 "precipitation": 35}
    print(t_wb.thornthwaite_water_balance(**t_wb_data))
    test_keys_2 = \
        sorted([i for i in t_wb.thornthwaite_water_balance().values()])

    print(test_keys_2)

    teste_cls_mtd = \
        ThornthwaiteWaterBalance.thornthwaite_wb_simple(100, 45, 35)
    print(teste_cls_mtd.thornthwaite_water_balance())
