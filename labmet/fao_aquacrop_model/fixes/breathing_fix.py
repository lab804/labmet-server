#!/usr/bin/env python
# -*- coding: utf-8 -*-

from labmet.labmetExceptions.labmetExceptions import InputTypeException

__author__ = 'joaotrevizoliesteves, Murilo Ijanc'
__copyright__ = "Copyright 2015, Lab804"
__license__ = "BSD"
__version__ = "0.1"


class BreathingFix(object):
    """Breathing Fix

    While photosynthesis and plant growth happens, part of
    the carbohydrates are used in the photorespiration process
    and tissues maintenance. This consumption is highly dependant on the
    ambient temperature. this class is used to fix it.

    :param temperature:

    :type temperature: int or float
    """

    def __init__(self, temperature):
        try:
            self.temperature = float(temperature)
        except:
            raise InputTypeException("The ho, temperature "
                                     "must be castable to float!")

    def breathing_fix(self):
        """
        Correção em si
        """
        if self.temperature >= 20.0:
            return 0.6
        else:
            return 0.5
