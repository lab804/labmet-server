#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'joaotrevizoliesteves, Murilo Ijanc'
__copyright__ = "Copyright 2015, Lab804"
__license__ = "BSD"
__version__ = "0.1"

import math
from ...labmetExceptions import InputTypeException


class WinterTemperatureFixCIII(object):
    """Winter Temperature Fix for C3 plants

    Fix for culture temperature, used in the
    potential productivity calculus, proposed
    by Barbieri & Tuon(1992) for winter cultures of
    C3 type.

    """
    def __init__(self, temperature):
        """Fix for the temperature

        Init method for the temperature fix classes

        :param temperature: The average period temperature (ºC)
        :type temperature: int or float
        """
        try:
            self.temperature = float(temperature)
        except:
            raise InputTypeException("The temperature must be int or float")

    def cloudy_days_fix(self):
        """Cloudy days fix

        Temperature fix for cloudy days

        :return

        """
        if 15.0 <= self.temperature <= 20.0:
            return 0.7 + 0.0035 * self.temperature - 0.001 * math.pow(self.temperature, 2)
        else:
            return 0.25 + 0.0875 * self.temperature - 0.0025 * math.pow(self.temperature, 2)

    def clear_days_fix(self):
        """Clear days fix

        Temperature fix for clear day

        """
        if 15.0 <= self.temperature <= 20.0:
            return 0.25 + 0.0875 * self.temperature - 0.0025 * math.pow(self.temperature, 2)
        else:
            return -0.5 + 0.175 * self.temperature - 0.005 * math.pow(self.temperature, 2)


class SummerTemperatureFixCIII(WinterTemperatureFixCIII):
    """
    Correção de temperatura de cultura, utilizada no
    calculo de produtividade potêncial, propostos por
    Barbieri & Tuon(1992) para culturas de verão do
    tipo CIII.
    """
    def cloudy_days_fix(self):
        """
        Correção de temperatura para céu nublado
        """
        if 16.5 <= self.temperature <= 37.0:
            return 0.583 + 0.014 * self.temperature\
                   + 0.0013 * math.pow(self.temperature, 2)\
                   - 0.000037 * math.pow(self.temperature, 3)
        else:
            return -0.0425 + 0.035 * self.temperature\
                   + 0.00325 * math.pow(self.temperature, 2)\
                   - 0.0000925 * math.pow(self.temperature, 3)

    def clear_days_fix(self):
        """
        Correção de temperatura para céu claro
        """
        if 16.5 <= self.temperature <= 37.0:
            return -0.0425 + 0.035 * self.temperature\
                   + 0.00325 * math.pow(self.temperature, 2)\
                   - 0.0000925 * math.pow(self.temperature, 3)
        else:
            return -1.085 + 0.07 * self.temperature\
                   + 0.0065 * math.pow(self.temperature, 2)\
                   - 0.000185 * math.pow(self.temperature, 3)


class TemperatureFixCIV(WinterTemperatureFixCIII):
    """
    Correção de temperatura de cultura, utilizada no
    calculo de produtividade potêncial, propostos por
    Barbieri & Tuon(1992) para culturas de verão do
    tipo CIV.
    """
    def cloudy_days_fix(self):
        """
        Correção de temperatura para céu nublado
        """
        if self.temperature >= 16.5:
            return -1.064 + 0.173 * self.temperature - 0.0029 * math.pow(self.temperature, 2)
        else:
            return -4.16 + 0.4325 * self.temperature - 0.00725 * math.pow(self.temperature, 2)

    def clear_days_fix(self):
        """
        Correção de temperatura para céu claro
        """
        if self.temperature < 16.5:
            return -4.16 + 0.4325 * self.temperature - 0.00725 * math.pow(self.temperature, 2)
        else:
            return -9.32 + 0.865 * self.temperature - 0.0145 * math.pow(self.temperature, 2)