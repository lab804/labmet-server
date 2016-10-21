#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""""Calculus for the crop evapotranspiration

Copyright 2016, Lab804

.. module: labmet.base.evapotranspiration.ETc.ETc
   :platform: Unix, Windows, macOS
   :synopsis: The methodology and algorithm for ETc calculus

.. moduleauthor:: João Trevizoli Esteves <joao@lab804.com.br>
"""

import tabulate

from base.labmetExceptions import InputException, InputRangeException
from functools import reduce


class ETcKcTable(object):
    _cultures = {
        "alfalfa1": {
            "establishment": [0.3, 0.4],
            "vegetative_growth": [1.0, 1.0],
            "flowering": [1.0, 1.0],
            "fruiting": [1.0, 1.0],
            "ripening": [1.05, 1.2]
        },
        "alfalfa2": {
            "establishment": [0.3, 0.4],
            "vegetative_growth": [1.0, 1.0],
            "flowering": [1.0, 1.0],
            "fruiting": [1.0, 1.0],
            "ripening": [1.05, 1.2]
        },
        "cotton": {
            "establishment": [0.4, 0.5],
            "vegetative_growth": [0.7, 0.8],
            "flowering": [0.7, 0.8],
            "fruiting": [0.8, 0.9],
            "ripening": [0.65, 0.7]
        },
        "peanut": {
            "establishment": [0.4, 0.5],
            "vegetative_growth": [0.7, 0.8],
            "flowering": [0.95, 1.1],
            "fruiting": [0.75, 0.85],
            "ripening": [0.55, 0.6]
        },
        "rice": {
            "establishment": [0.4, 0.5],
            "vegetative_growth": [0.7, 0.8],
            "flowering": [0.9, 1.2],
            "fruiting": [0.8, 0.9],
            "ripening": [0.5, 0.6]
        },

        "banana_tropical": {
            "establishment": [0.4, 0.5],
            "vegetative_growth": [0.7, 0.85],
            "flowering": [1.0, 1.1],
            "fruiting": [0.9, 1.0],
            "ripening": [0.75, 0.85]
        },
        "banana_subtropical": {
            "establishment": [0.5, 0.65],
            "vegetative_growth": [0.8, 0.9],
            "flowering": [1.0, 1.2],
            "fruiting": [1.0, 1.15],
            "ripening": [1.0, 1.15]
        },
        "potato": {
            "establishment": [0.4, 0.5],
            "vegetative_growth": [0.7, 0.8],
            "flowering": [1.05, 1.2],
            "fruiting": [0.85, 0.95],
            "ripening": [0.7, 0.75]
        },
        "beet": {
            "establishment": [0.4, 0.5],
            "vegetative_growth": [0.75, 0.85],
            "flowering": [1.05, 1.2],
            "fruiting": [0.9, 1.0],
            "ripening": [0.6, 0.7]
        },
        "sugarcane": {
            "establishment": [0.4, 0.5],
            "vegetative_growth": [0.7, 1.0],
            "flowering": [1.0, 1.3],
            "fruiting": [0.75, 0.8],
            "ripening": [0.5, 0.6]
        },
        "onion": {
            "establishment": [0.4, 0.6],
            "vegetative_growth": [0.7, 0.8],
            "flowering": [0.95, 1.1],
            "fruiting": [0.85, 0.9],
            "ripening": [0.85, 0.9]
        },
        "onion_wet": {
            "establishment": [0.4, 0.6],
            "vegetative_growth": [0.6, 0.75],
            "flowering": [0.95, 1.05],
            "fruiting": [0.95, 1.05],
            "ripening": [0.95, 1.05]
        },
        "coffee": {
            "establishment": [1.0, 1.0],
            "vegetative_growth": [1.0, 1.0],
            "flowering": [0.65, 0.8],
            "fruiting": [1.0, 1.0],
            "ripening": [1.0, 1.0]
        },
        "coffee_untreated": {
            "establishment": [1.0, 1.0],
            "vegetative_growth": [1.0, 1.0],
            "flowering": [0.85, 0.9],
            "fruiting": [1.0, 1.0],
            "ripening": [1.0, 1.0]
        },

        "citrus": {
            "establishment": [1.0, 1.0],
            "vegetative_growth": [1.0, 1.0],
            "flowering": [0.65, 0.75],
            "fruiting": [1.0, 1.0],
            "ripening": [1.0, 1.0]
        },
        "citrus_untreated": {
            "establishment": [1.0, 1.0],
            "vegetative_growth": [1.0, 1.0],
            "flowering": [0.65, 0.75],
            "fruiting": [1.0, 1.0],
            "ripening": [1.0, 1.0]
        },
        "pea_grain": {
            "establishment": [0.4, 0.5],
            "vegetative_growth": [0.7, 0.85],
            "flowering": [1.05, 1.2],
            "fruiting": [1.0, 1.15],
            "ripening": [0.95, 1.1]
        },
        "pea_legume": {
            "establishment": [0.4, 0.5],
            "vegetative_growth": [0.7, 0.85],
            "flowering": [1.05, 1.2],
            "fruiting": [1.0, 1.15],
            "ripening": [0.95, 1.1]
        },
        "bean": {
            "establishment": [0.3, 0.4],
            "vegetative_growth": [0.7, 0.8],
            "flowering": [1.05, 1.2],
            "fruiting": [0.65, 0.75],
            "ripening": [0.25, 0.3]
        },
        "green_bean": {
            "establishment": [0.3, 0.4],
            "vegetative_growth": [0.65, 0.75],
            "flowering": [0.95, 1.05],
            "fruiting": [0.9, 0.95],
            "ripening": [0.85, 0.95]
        },
        "sunflower": {
            "establishment": [0.3, 0.4],
            "vegetative_growth": [0.7, 0.8],
            "flowering": [1.05, 1.2],
            "fruiting": [0.7, 0.8],
            "ripening": [0.35, 0.45]
        },
        "watermelon": {
            "establishment": [0.4, 0.5],
            "vegetative_growth": [0.7, 0.8],
            "flowering": [0.95, 1.05],
            "fruiting": [0.8, 0.9],
            "ripening": [0.65, 0.75]
        },
        "sweet_corn": {
            "establishment": [0.3, 0.5],
            "vegetative_growth": [0.7, 0.9],
            "flowering": [1.05, 1.2],
            "fruiting": [1.0, 1.15],
            "ripening": [0.9, 1.1]
        },
        "corn": {
            "establishment": [0.3, 0.5],
            "vegetative_growth": [0.7, 0.85],
            "flowering": [1.05, 1.2],
            "fruiting": [0.8, 0.95],
            "ripening": [0.55, 0.6]
        },
        "olive": {
            "establishment": [1.0, 1.0],
            "vegetative_growth": [1.0, 1.0],
            "flowering": [0.4, 0.6],
            "fruiting": [1.0, 1.0],
            "ripening": [1.0, 1.0]
        },
        "pepper": {
            "establishment": [0.3, 0.4],
            "vegetative_growth": [0.6, 0.75],
            "flowering": [0.95, 1.1],
            "fruiting": [0.85, 1.0],
            "ripening": [0.8, 0.9]
        },
        "pepper_green": {
            "establishment": [0.3, 0.4],
            "vegetative_growth": [0.6, 0.75],
            "flowering": [0.95, 1.1],
            "fruiting": [0.85, 1.0],
            "ripening": [0.8, 0.9]
        },
        "cabbage": {
            "establishment": [0.4, 0.5],
            "vegetative_growth": [0.7, 0.8],
            "flowering": [0.95, 1.1],
            "fruiting": [0.9, 1.0],
            "ripening": [0.8, 0.95]
        },
        "rubber_tree": {
            "establishment": [1.0, 1.0],
            "vegetative_growth": [1.0, 1.0],
            "flowering": [0, 7, 1, 2],
            "fruiting": [1.0, 1.0],
            "ripening": [1.0, 1.0]
        },
        "soy": {
            "establishment": [0.3, 0.4],
            "vegetative_growth": [0.7, 0.8],
            "flowering": [1.0, 1.15],
            "fruiting": [0.7, 0.8],
            "ripening": [0.4, 0.5]
        },
        "sorghum": {
            "establishment": [0.3, 0.4],
            "vegetative_growth": [0.7, 0.75],
            "flowering": [1.0, 1.15],
            "fruiting": [0.75, 0.8],
            "ripening": [0.5, 0.55]
        },
        "tobacco": {
            "establishment": [0.3, 0.4],
            "vegetative_growth": [0.7, 0.8],
            "flowering": [1.0, 1.2],
            "fruiting": [0.9, 1.0],
            "ripening": [0.75, 0.85]
        },
        "tomato": {
            "establishment": [0.4, 0.5],
            "vegetative_growth": [0.7, 0.8],
            "flowering": [1.05, 1.25],
            "fruiting": [0.8, 0.95],
            "ripening": [0.6, 0.65]
        },
        "wheat": {
            "establishment": [0.3, 0.4],
            "vegetative_growth": [0.7, 0.8],
            "flowering": [1.05, 1.2],
            "fruiting": [0.65, 0.75],
            "ripening": [0.2, 0.25]
        },
        "grape": {
            "establishment": [0.35, 0.55],
            "vegetative_growth": [0.6, 0.8],
            "flowering": [0.7, 0.9],
            "fruiting": [0.6, 0.8],
            "ripening": [0.55, 0.7]
        }
    }

    def all_cultures_table(self, print_table=True, tablefmt="fancy_grid"):
        """All cultures table

        Create a string with a table with all
        the possible cultures with its life stages
        Kcs

        :return: A table with all cultures
        :rtype: str
        """
        culture_table = [[
                          k,
                          "{} - {}".format(v["establishment"][0],
                                           v["establishment"][1]),
                          "{} - {}".format(v["vegetative_growth"][0],
                                           v["vegetative_growth"][1]),
                          "{} - {}".format(v["flowering"][0],
                                           v["flowering"][1]),
                          "{} - {}".format(v["fruiting"][0],
                                           v["fruiting"][1]),
                          "{} - {}".format(v["ripening"][0],
                                           v["ripening"][1])
                         ] for k, v in self._cultures.items()]
        headers = ["Culture", "Establishment Kc",
                   "Vegetative Growth Kc", "Flowering Kc",
                   "Fruiting Kc", "Ripening Kc"]
        table = tabulate.tabulate(sorted(culture_table),
                                  headers, tablefmt=tablefmt)
        if print_table:
            print(table)

        return table


class ETcKc(ETcKcTable):
    def __init__(self, culture):
        self.culture = culture

    @property
    def culture(self):
        return self.__culture

    @culture.setter
    def culture(self, culture):
        if culture in self._cultures:
            culture_name = {"name": culture}
            culture_name.update(self._cultures[culture])
            self.__culture = culture_name
        else:
            culture_table = [[k]
                             for k in self._cultures.keys()]
            headers = ["culture"]
            table = tabulate.tabulate(sorted(culture_table),
                                      headers, tablefmt="fancy_grid")
            raise InputException("culture not found, check the table with "
                                 "all the available cultures and choose one: "
                                 "\n{}".format(table))

    @staticmethod
    def __average_calculator(interval_list):
        """" Average calculator

        Calculate the limits average for the culture coefficients
        in all life stages

        :return average Kc
        :rtype float
        """
        return reduce(lambda x, y: x + y, interval_list) / len(interval_list)

    def crop_coefficients(self, rh_percent=None, wind_speed=None):

        establishment = self.culture["establishment"]
        vegetative_growth = self.culture["vegetative_growth"]
        flowering = self.culture["flowering"]
        fruiting = self.culture["fruiting"]
        ripening = self.culture["ripening"]

        if rh_percent is None or wind_speed is None:
            return {"establishment": self.__average_calculator(establishment),
                    "vegetative_growth": self.__average_calculator(vegetative_growth),
                    "flowering": self.__average_calculator(flowering),
                    "fruiting": self.__average_calculator(fruiting),
                    "ripening": self.__average_calculator(ripening)}
        else:
            if 0.0 > rh_percent > 100.0:
                raise InputRangeException("The relative humidity must be greater"
                                          " or equal than 0.0,  or lower or equal than 100")
            if rh_percent > 70.0 and wind_speed < 5.0:
                kc_dict = {"establishment": establishment[0],
                           "vegetative_growth": vegetative_growth[0],
                           "flowering": flowering[0],
                           "fruiting": fruiting[0],
                           "ripening": ripening[0]}
            elif rh_percent < 70.00 and wind_speed > 5.0:
                kc_dict = {"establishment": establishment[1],
                           "vegetative_growth": vegetative_growth[1],
                           "flowering": flowering[1],
                           "fruiting": fruiting[1],
                           "ripening": ripening[1]}
            else:
                kc_dict = {"establishment": self.__average_calculator(establishment),
                           "vegetative_growth": self.__average_calculator(vegetative_growth),
                           "flowering": self.__average_calculator(flowering),
                           "fruiting": self.__average_calculator(fruiting),
                           "ripening": self.__average_calculator(ripening)}
            return kc_dict

    def chosen_culture_table(self, print_table=True, tablefmt="fancy_grid"):
        """Chosen cultures table

        Create a string with a table with the
        chosen culture name and its crop
        coefficients.

        :return: A table the chosen culture fixes
        :rtype: str
        """
        culture_table = [["Culture Name",
                          self.culture["name"]],
                         ["Min Establishment Kc",
                          self.culture["establishment"][0]],
                         ["Max Establishment Kc",
                          self.culture["establishment"][1]],
                         ["Average Establishment Kc",
                          self.__average_calculator(
                              self.culture["establishment"]
                          )],
                         ["Min Vegetative Growth Kc",
                          self.culture["vegetative_growth"][0]],
                         ["Max Vegetative Growth Kc",
                          self.culture["vegetative_growth"][1]],
                         ["Average Vegetative Growth Kc",
                          self.__average_calculator(
                              self.culture["vegetative_growth"]
                          )],
                         ["Min Flowering Kc",
                          self.culture["flowering"][0]],
                         ["Max flowering Kc",
                          self.culture["flowering"][1]],
                         ["Average FloweringKc",
                          self.__average_calculator(
                              self.culture["flowering"]
                          )],
                         ["Min Fruiting Kc",
                          self.culture["fruiting"][0]],
                         ["Max Fruiting Kc",
                          self.culture["fruiting"][1]],
                         ["Average Fruiting Kc",
                          self.__average_calculator(
                              self.culture["fruiting"]
                          )],
                         ["Min Ripening Kc",
                          self.culture["ripening"][0]],
                         ["Max Ripening Kc",
                          self.culture["ripening"][1]],
                         ["Average Ripening Kc",
                          self.__average_calculator(
                              self.culture["ripening"]
                          )]
                         ]
        headers = ["culture fix indexes", "values"]

        table = tabulate.tabulate(culture_table,
                                  headers, tablefmt=tablefmt)
        if print_table:
            print(table)

        return table

    def __str__(self):
        return self.chosen_culture_table()

if __name__ == '__main__':
    culture_teste = {
        "culture": "soy"
    }
    colheita = ETcKc(**culture_teste)
    colheita.chosen_culture_table()
    print(colheita.crop_coefficients())
