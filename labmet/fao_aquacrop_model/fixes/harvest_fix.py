#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Calculus for the harvested part fix

Copyright 2016, Lab804

.. module: labmet.base.fao_aquacrop_model.fixes.harvested_fix
   :platform: Unix, Windows, macOS
   :synopsis: All the calculus for the harvested part.

.. moduleauthor:: João Trevizoli Esteves <joao@lab804.com.br>
"""

import tabulate

from functools import reduce
from ...labmetExceptions import InputException

__author__ = 'joaotrevizoliesteves, Murilo Ijanc'
__copyright__ = "Copyright 2015, Lab804"
__license__ = "BSD"
__version__ = "0.1"


class HarvestPartFixTable(object):

    _cultures = {
        "banana_tropical": {
            "harvested_part": "fruit",
            "harvest_part_limits": [1, 1],
            "humidity_limits": [70, 80]
        },
        "banana_subtropical": {
            "harvested_part": "fruit",
            "harvest_part_limits": [1, 1],
            "humidity_limits": [70, 80]
        },
        "citrus": {
            "harvested_part": "fruit",
            "harvest_part_limits": [1, 1],
            "humidity_limits": [70, 85]
        },
        "pineapple": {
            "harvested_part": "fruit",
            "harvest_part_limits": [0.50, 0.60],
            "humidity_limits": [80.00, 85.00]
        },
        "alfalfa1": {
            "harvested_part": "hay",
            "harvest_part_limits": [0.40, 0.50],
            "humidity_limits": [10.00, 15.00]
        },
        "alfalfa2": {
            "harvested_part": "hay",
            "harvest_part_limits": [0.80, 0.90],
            "humidity_limits": [10.00, 15.00]
        },
        "grape": {
            "harvested_part": "fruit",
            "harvest_part_limits": [1.00, 1.00],
            "humidity_limits": [20.00, 20.00]
        },
        "cotton": {
            "harvested_part": "fiber",
            "harvest_part_limits": [0.08, 0.12],
            "humidity_limits": [0.00, 0.00]
        },
        "peanut": {
            "harvested_part": "grain",
            "harvest_part_limits": [0.25, 0.35],
            "humidity_limits": [15.00, 15.00]
        },
        "rice": {
            "harvested_part": "grain",
            "harvest_part_limits": [0.40, 0.50],
            "humidity_limits": [15.00, 20.00]
        },
        "potato": {
            "harvested_part": "tuber",
            "harvest_part_limits": [0.55, 0.65],
            "humidity_limits": [70.00, 75.00]
        },
        "beet": {
            "harvested_part": "sugar",
            "harvest_part_limits": [0.35, 0.45],
            "humidity_limits": [80.00, 85.00]
        },
        "sugarcane": {
            "harvested_part": "sugar",
            "harvest_part_limits": [0.70, 0.80],
            "humidity_limits": [80.00, 80.00]
        },
        "onion": {
            "harvested_part": "bulb",
            "harvest_part_limits": [0.20, 0.30],
            "humidity_limits": [85.00, 90.00]
        },
        "pea_grain": {
            "harvested_part": "grain",
            "harvest_part_limits": [0.30, 0.40],
            "humidity_limits": [10.00, 10.00]
        },
        "pea_legume": {
            "harvested_part": "legume",
            "harvest_part_limits": [0.30, 0.40],
            "humidity_limits": [10.00, 10.00]
        },
        "bean": {
            "harvested_part": "grain",
            "harvest_part_limits": [1, 1],
            "humidity_limits": [70.00, 80.00]
        },
        "olive": {
            "harvested_part": "fruit",
            "harvest_part_limits": [1.00, 1.00],
            "humidity_limits": [30.00, 30.00]
        },
        "sunflower": {
            "harvested_part": "seed",
            "harvest_part_limits": [0.20, 0.30],
            "humidity_limits": [10.00, 15.00]
        },
        "corn": {
            "harvested_part": "grain",
            "harvest_part_limits": [0.35, 0.45],
            "humidity_limits": [10.00, 13.00]
        },
        "pepper": {
            "harvested_part": "fruit",
            "harvest_part_limits": [0.20, 0.40],
            "humidity_limits": [90.00, 90.00]
        },
        "cabbage": {
            "harvested_part": "head",
            "harvest_part_limits": [0.60, 0.70],
            "humidity_limits": [90.00, 90.00]
        },
        "soy": {
            "harvested_part": "grain",
            "harvest_part_limits": [0.30, 0.40],
            "humidity_limits": [6.00, 10.00]
        },
        "sorghum": {
            "harvested_part": "grain",
            "harvest_part_limits": [0.30, 0.40],
            "humidity_limits": [12.00, 15.00]
        },
        "tomato": {
            "harvested_part": "fruit",
            "harvest_part_limits": [0.25, 0.35],
            "humidity_limits": [80.00, 90.00]
        },
        "watermelon": {
            "harvested_part": "fruit",
            "harvest_part_limits": [1, 1],
            "humidity_limits": [90.00, 90.00]
        },
        "wheat": {
            "harvested_part": "grain",
            "harvest_part_limits": [0.35, 0.45],
            "humidity_limits": [12.00, 15.00]
        }
    }

    def all_cultures_table(self, print_table=True, tablefmt="fancy_grid"):
        """All cultures table

        Create a string with a table with all
        the possible cultures with its fixes and
        harvested part

        :return: A table with all cultures
        :rtype: str
        """
        culture_table = [[
                          k,
                          v["harvested_part"],
                          "{} - {}".format(v["harvest_part_limits"][0],
                                           v["harvest_part_limits"][1]),
                          "{}% - {}%".format(v["humidity_limits"][0],
                                             v["humidity_limits"][1])
                         ] for k, v in self._cultures.items()]
        headers = ["culture", "harvested part",
                   "harvested part fix", "humidity fix"]
        table = tabulate.tabulate(sorted(culture_table),
                                  headers, tablefmt=tablefmt)
        if print_table:
            print(table)

        return table


class HarvestedPartFix(HarvestPartFixTable):
    """Harvested Part Fix

    Correction for the harvested part, for example the soy beans,
    sugar-cane culms and so on. It were used the methodology and the
    tables proposed by Doorembos & Kassam (1994) and Barbieri & Tuon (1992).

    """

    def __init__(self, culture):
        """Gets the chosen culture from a dict

        ..note:: The culuture that you are going to use must be in the table


        :param culture:
        """
        self.culture = culture

    @property
    def culture(self):
        return self.__culture

    @culture.setter
    def culture(self, culture):
        if culture in self._cultures:
            culture_name = {"name": culture.lower()}
            culture_name.update(self._cultures[culture])
            self.__culture = culture_name
        else:
            culture_table = [[k, v["harvested_part"]]
                             for k, v in self._cultures.items()]
            headers = ["culture", "haversted part"]
            table = tabulate.tabulate(sorted(culture_table),
                                      headers, tablefmt="fancy_grid")
            raise InputException("culture not found, check the table with "
                                 "all the available cultures: \n{}".format(table))

    @staticmethod
    def __average_calculator(interval_list):
        """" Average calculator

        Calculate the limits average for both harvested part
        moisture fix and harvested part fix

        :return average moisture fix or harvest part fix
        :rtype float
        """
        return reduce(lambda x, y: x + y, interval_list) / len(interval_list)

    def humidity_fix(self):
        """ Humidity fix

        gets the humidity fix and calculates its
        average based on the chosen culture.

        ..note::
            The table with the fixes for the harvested part and
            for the humidity were picked from the FAO model description by
            Doorenbos & Kassam (1994) and by the Barbieri & T uon (1992) paper.

        :return: A dict with the harvested part name and
         the minimum, maximum and average humidity fix.
        :rtype: dict
        """
        part = self.culture["harvested_part"]
        humidity = self.culture['humidity_limits']
        average = self.__average_calculator(humidity)
        return {
                "part": part,
                "minimum": humidity[0],
                "average": average,
                "maximum": humidity[-1]
               }

    def harvested_part_fix(self):
        """ Harvested part fix

        gets the harvested part fix and
        calculates its average based
        on the chosen culture.

        ..note::
            The table with the fixes for the harvested part and
            for the humidity were picked from the FAO model description by
            Doorenbos & Kassam (1994) and by the Barbieri & T uon (1992) paper.

        :return: A dict with the harvested part name and
        the minimum, maximum and average harvested part fixes
        :rtype: dict
        """
        part = self.culture["harvested_part"]
        harvest_part_limits = self.culture["harvest_part_limits"]
        average = self.__average_calculator(harvest_part_limits)
        return {
                "part": part,
                "minimum": harvest_part_limits[0],
                "maximum": harvest_part_limits[-1],
                "average": average
               }

    def chosen_culture_table(self, tablefmt="fancy_grid"):
        """Chosen cultures table

        Create a string with a table with the
        chosen culture name, harvested part and
        its fixes.

        :return: A table the chosen culture fixes
        :rtype: str
        """
        culture_table = [["culture name",
                          self.culture["name"]],
                         ["culture  harvested part",
                          self.culture["harvested_part"]],
                         ["min harvested part fix",
                          self.culture["harvest_part_limits"][0]],
                         ["max harvested part fix",
                          self.culture["harvest_part_limits"][1]],
                         ["average harvested part fix",
                          self.__average_calculator(
                              self.culture["harvest_part_limits"]
                          )],
                         ["min humidity fix",
                          self.culture["humidity_limits"][0]],
                         ["max humidity fix",
                          self.culture["humidity_limits"][1]],
                         ["average humidity fix",
                          self.__average_calculator(
                              self.culture["humidity_limits"]
                          )]
                         ]
        headers = ["culture fix indexes", "values"]
        return tabulate.tabulate(culture_table,
                                 headers, tablefmt=tablefmt)

    def __str__(self):
        return self.chosen_culture_table()
