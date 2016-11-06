#!/usr/bin/env python
# -*- coding: utf-8 -*-

from labmet.labmetExceptions.labmetExceptions import InputException, InputTypeException
from labmet.radiation.radiation import ExtraterrestrialIrradiance
from labmet.fao_aquacrop_model.fixes.temperature_fix import *
from labmet.fao_aquacrop_model.fixes.breathing_fix import BreathingFix
from labmet.fao_aquacrop_model.fixes.leaf_area_fix import LeafAreaIndexFix
from labmet.fao_aquacrop_model.fixes.harvest_fix import HarvestedPartFix, HarvestPartFixTable
from labmet.evapotranspiration.ETo.thornthwaite import ThornthwaiteETo
from datetime import datetime


from labmet.fao_aquacrop_model.fixes.input_variable_fix import *

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
            return clear_pot_prod / 10000.00

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
        if eto != 0:
            obtainable_productivity = (1 - self.ky * (1 - etc / eto)) * potential_productivity
            if obtainable_productivity > 0:
                return obtainable_productivity
            return 0
        else:
            return 0


class AquaCropModel(ObtainableProductivity):
    """AquaCrop Model

    This class is a wrapper to use the AquaCrop model
    directly with data coming from the weather station.

    ..note:: To the model work in such a short period of time
             many assumptions had to be done, and this class needs
             improvements

    """
    def __init__(self, culture_name, ky, lat, eto_culture, avg_year_temp,
                 n_days, peak_l_a_index, awc, soil_moisture=None,
                 precipitation=0):
        """AquaCropModel init method

        Instantiation of the aquacrop model.

        ..note:: Only static params are used as input
                 for the class initialization

        :param culture_name: The name of the culture
        :param ky: The culture coefficient
        :param lat: The latitude in decimal degrees
        :param eto_culture: The relative
         culture evapotranspiration
        :param avg_year_temp: The location norma
         temperature
        :param n_days: The number of days in
         the culture life cycle
        :param peak_l_a_index: The peak leaf area index
        :param awc: The Available water content
        :param soil_moisture: The initial soil moisture
        :param precipitation: The initial precipitation

        :type culture_name: str
        :type ky: float
        :type lat: float
        :type eto_culture: float
        :type avg_year_temp: int or float
        :type n_days: int
        :type peak_l_a_index: int or float
        :type awc: int or float
        :type soil_moisture: int or float
        :type precipitation: int or float
        """
        self.ky = ky
        self.lat = lat
        self.eto_culture = eto_culture
        self.avg_year_temp =avg_year_temp
        self.n_days = n_days
        self.peak_l_a_index = peak_l_a_index
        self.awc = awc
        self.precipitation = precipitation
        self.__eto = None
        self.__etc = None

        if soil_moisture is None:
            self.soil_moisture = self.awc
        else:
            self.soil_moisture = soil_moisture
        if HarvestPartFixTable().has_culture_table(culture_name):
            self.culture_name = culture_name
        else:
            raise InputException("Your culture is not available for the model now!")

        ObtainableProductivity.__init__(self, ky)

    def __get_radiation_data(self, date=datetime.now()):
        """Get radiation data

        This method calculates the extraterrestrial radiation
        in the latitude point that the culture is established
        by calling the ExtraterrestrialIrradiance class

        :param date: The desired datetime(default=datetime.now())

        :type date: datetime

        :return: a dict with the radiation values
        :rtype: dict
        """
        radiation_data = {"day": date,
                          "lat": self.lat}
        extra_radiation = ExtraterrestrialIrradiance(**radiation_data)

        return {"radiation": extra_radiation.ho_cal_sqaured_cm(),
                "photoperiod": extra_radiation.photoperiod()}

    def __set_et(self, photoperiod, temperature):
        """Set Evapotranspiration

        This method sets and updates the evapotranspiration
        value (__eto) by utilizing the method proposed by thornthwaite

        ..note:: If the __etc is set to None this method will update its
                 value with the vaue of the __eto

        :param photoperiod: The photoperiod of the desired day
        :param temperature: The air temperature in ºC

        :type photoperiod: int or float
        :type temperature: int or float

        """
        eto = ThornthwaiteETo(temperature,
                              photoperiod,
                              30,
                              self.avg_year_temp).eto_day() * self.eto_culture
        self.__eto = eto
        if self.__etc is None:
            self.__etc = self.__eto

    @staticmethod
    def __get_temperature_fix(air_temperature, culture_type, culture_season):
        """Get Temperature fix

        This method gets the fix for the desired type of
        culture given a season and the air temperature

        :param air_temperature: The air temperature in ºC
        :param culture_type: The culture type (c3 or c4)
        :param culture_season: The season of culture growth (winter or summer)

        :type air_temperature: int or float
        :type culture_type: str
        :type culture_season: str

        :return: A dict with the temperature fix
         for cloudy and clear days
        :rtype: dict

        """
        culture_type = culture_type.lower()

        if culture_type == "c3":
            if culture_season == "summer":
                temp_fix = SummerTemperatureFixCIII(temperature=air_temperature)
            elif culture_season == "winter":
                temp_fix = WinterTemperatureFixCIII(temperature=air_temperature)
            else:
                raise InputException("The seasen must be a string "
                                     "containing winter or summer")
        elif culture_type == "c4":
            temp_fix = TemperatureFixCIV(temperature=air_temperature)
        else:
            raise InputException("The culture must be of type c3 or c4")

        return {"temp_cloudy_days_fix": temp_fix.cloudy_days_fix(),
                "temp_clear_days_fix": temp_fix.clear_days_fix()}

    def __get_potential_productivity(self, extra_radiation, illuminance, temperature, culture_type, culture_season):
        """Gets the Potential productivity

        This method calculates the potential productivity
        through the method described in the AquaCrop model

        :param extra_radiation: The extraterrestrial irradiation in cal . day⁻2
        :param illuminance: The illuminance in lx
        :param temperature: The temperature in ºC
        :param culture_type: The culture type (c3 or c4)
        :param culture_season: The season of culture growth (winter or summer)

        :type extra_radiation: int or float
        :type illuminance: int or float
        :type temperature: int or float
        :type culture_type: str
        :type culture_season: str


        :return: The potential productivity in hectometers . m⁻2
        :rtype: float
        """
        temp_fix = self.__get_temperature_fix(air_temperature=temperature,
                                              culture_type=culture_type,
                                              culture_season=culture_season)

        potential_productivity = \
            PotentialProductivity(extra_radiation,
                                  temp_cloudy_days_fix=temp_fix["temp_cloudy_days_fix"],
                                  temp_clear_days_fix=temp_fix["temp_clear_days_fix"],
                                  n_N=self.lux_to_n_N(illuminance))

        breath_fix = BreathingFix(temperature=temperature).breathing_fix()
        harvest_fix = HarvestedPartFix(self.culture_name).harvested_part_fix()["average"]
        leaf_area_fix = LeafAreaIndexFix(self.peak_l_a_index).leaf_area_index_fix()

        potential_productivity = potential_productivity.potential_productivity(leaf_area_fix,
                                                                               breath_fix,
                                                                               harvest_fix,
                                                                               self.n_days,
                                                                               hectometer_sqr_m=True)
        if potential_productivity > 0:
            return potential_productivity
        return 0

    @staticmethod
    def lux_to_n_N(lux):
        """Lux to n/N

        Computes the ratio between sunny
         and cloudy days

        :param lux: The measured amount of lumens
        :return: Lumens to cloudy/sunny ratio
        :rtype: float
        """
        if lux > 20000.0:
            return 1.0
        else:
            return float(lux) / 20000.0

    def soil_moisture_to_mm(self, percentage):
        """Soil moisture to mm

        Converts the percentage soil moisture
        into mm, ie converts the percentage
        to the amount of water inside the
        awc(Available Water Content)

        :param percentage: Soil moisture percentage
        :param awc: Soil Water content

        :type percentage: int or float
        :type awc: float

        :return: Soil Moisture im mm
        :rtype: int or float
        """
        if percentage > 100.0:
            percentage = 100.0
        elif percentage < 0.0:
            percentage = 0.0
        return self.awc * float(percentage) / 100.0

    def aqua_crop(self, soil_moisture, temperature, illuminance,
                  date=datetime.now(), culture_type="c3", culture_season="summer"):
        """Aqua Crop

        This is the main method and unique public
        method of this class, when calling this method
        the yields are calculated and returned inside a dict

        ..warning: When this method is called all the __etc, __eto
                   and precipitation values are updated insed the
                   class for the next call.

        :param soil_moisture: The soil moisture measured in the sensor
        :param temperature: The air temperature in ºC
        :param illuminance: The illuminance in lx
        :param date: The datetime of the desired day(default=datetime.now())
        :param culture_type: The culture type (c3 or c4)
        :param culture_season: The season of culture growth (winter or summer)

        :type soil_moisture: int or float
        :type temperature: int or float
        :type illuminance: int or float
        :type date: datetime
        :type culture_type: str
        :type culture_season: str

        :return: A dict with the potential
        evapotranspiration(eto),
        culture evapotranspiration(etc),
        precipitation,
        potential productivity(potential_productivity)
        and obtainable productivity(obtainable_productivity)
        :rtype: dict

        """
        radiation_reading = self.__get_radiation_data(date=date)
        self.__set_et(photoperiod=radiation_reading["photoperiod"], temperature=temperature)

        potential_productivity = self.__get_potential_productivity(extra_radiation=radiation_reading["radiation"],
                                                                   illuminance=illuminance,
                                                                   temperature=temperature,
                                                                   culture_type=culture_type,
                                                                   culture_season=culture_season)
        obtainable_productivity = self.obtainable_productivity(eto=self.__eto,
                                                               etc=self.__etc,
                                                               potential_productivity=potential_productivity)

        soil_moisture_reading = self.soil_moisture_to_mm(soil_moisture)
        variation = soil_moisture_reading - self.soil_moisture
        if soil_moisture_reading > self.__eto:
            self.__etc = self.__eto
            if variation >= self.awc:
                self.precipitation = self.awc
            else:
                self.precipitation = variation
        else:
            self.precipitation = 0
            self.__etc = soil_moisture_reading
        self.soil_moisture = soil_moisture_reading

        return {"eto": self.__eto,
                "etc": self.__etc,
                "precipitation": self.precipitation,
                "potential_productivity": potential_productivity,
                "obtainable_productivity": obtainable_productivity}

# if __name__ == '__main__':
#     aquacrop_data = {"culture_name": "potato",
#                      "ky": 1.1,
#                      "lat": 51.5044968,
#                      "eto_culture": 0.8,
#                      "avg_year_temp": 19,
#                      "n_days": 130,
#                      "peak_l_a_index": 3,
#                      "awc": 35}
#
#     json_msg = {"collected_at": "2016-10-26T00:14:41",
#                 "bmp180_temp": 22.17,
#                 "bmp180_alt": -110.93,
#                 "bmp180_press": 1.03e3,
#                 "ds18b20_temp": 22.12,
#                 "dht22_temp": 23.20,
#                 "dht22_humid": 54.80,
#                 "bh1750_illuminance": 60,
#                 "analog_soil_moisture": 100}
#
#     teste_aqua_crop = AquaCropModel(**aquacrop_data)
#     print teste_aqua_crop.aqua_crop(soil_moisture=json_msg["analog_soil_moisture"],
#                                     date=datetime.now(),
#                                     temperature=json_msg["ds18b20_temp"],
#                                     illuminance=json_msg["bh1750_illuminance"])
#
#     json_msg = {"collected_at": "2016-10-26T00:14:41",
#                 "bmp180_temp": 22.17,
#                 "bmp180_alt": -110.93,
#                 "bmp180_press": 1.03e3,
#                 "ds18b20_temp": 22.12,
#                 "dht22_temp": 23.20,
#                 "dht22_humid": 54.80,
#                 "bh1750_illuminance": 60,
#                 "analog_soil_moisture": 3}
#
#     print teste_aqua_crop.aqua_crop(soil_moisture=json_msg["analog_soil_moisture"],
#                                     date=datetime.now(),
#                                     temperature=json_msg["ds18b20_temp"],
#                                     illuminance=json_msg["bh1750_illuminance"])
#
#     json_msg = {"collected_at": "2016-10-26T00:14:41",
#                 "bmp180_temp": 22.17,
#                 "bmp180_alt": -110.93,
#                 "bmp180_press": 1.03e3,
#                 "ds18b20_temp": 30.12,
#                 "dht22_temp": 23.20,
#                 "dht22_humid": 54.80,
#                 "bh1750_illuminance": 30000,
#                 "analog_soil_moisture": 100}
#
#     print teste_aqua_crop.aqua_crop(soil_moisture=json_msg["analog_soil_moisture"],
#                                     date=datetime.now(),
#                                     temperature=json_msg["ds18b20_temp"],
#                                     illuminance=json_msg["bh1750_illuminance"])
#     json_msg = {"collected_at": "2016-10-26T00:14:41",
#                 "bmp180_temp": 22.17,
#                 "bmp180_alt": -110.93,
#                 "bmp180_press": 1.03e3,
#                 "ds18b20_temp": 19,
#                 "dht22_temp": 23.20,
#                 "dht22_humid": 54.80,
#                 "bh1750_illuminance": 60,
#                 "analog_soil_moisture": 100}
#
#     print teste_aqua_crop.aqua_crop(soil_moisture=json_msg["analog_soil_moisture"],
#                                     date=datetime.now(),
#                                     temperature=json_msg["ds18b20_temp"],
#                                     illuminance=json_msg["bh1750_illuminance"])
