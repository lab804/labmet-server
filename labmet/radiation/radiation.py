#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from datetime import datetime

from labmet.labmetExceptions.labmetExceptions import InputTypeException
from labmet.radiation.factors import Photoperiod


class RadiationTableMethod(object):
    """Radiation Table Method

    Calculus of the solar global extraterrestrial irradiation
    in equivalent mm of evaporation by day

    """

    __lat_sul = {
             0: [14.5, 15.0, 15.2, 14.7, 13.9, 13.4, 13.5, 14.2, 14.9, 14.9, 14.6, 14.3],
             2: [14.8, 15.2, 15.2, 14.5, 13.6, 13.0, 13.2, 14.0, 14.8, 15.0, 14.8, 14.6],
             4: [15.0, 15.3, 15.1, 14.3, 13.3, 12.7, 12.8, 13.7, 14.7, 15.1, 15.0, 14.9],
             6: [15.3, 15.4, 15.1, 14.1, 13.0, 12.6, 12.5, 13.5, 14.6, 15.2, 15.2, 15.1],
             8: [15.6, 15.6, 15.0, 14.0, 12.7, 12.0, 12.2, 13.2, 14.5, 15.3, 15.4, 15.4],
            10: [15.9, 15.7, 15.0, 13.8, 12.4, 11.6, 11.9, 13.0, 14.4, 15.3, 15.7, 15.7],
            12: [16.1, 15.8, 14.9, 13.5, 12.0, 11.2, 11.5, 12.7, 14.2, 15.3, 15.8, 16.0],
            14: [16.3, 15.8, 14.9, 13.2, 11.6, 10.8, 11.1, 12.4, 14.0, 15.3, 15.9, 16.2],
            16: [16.5, 15.9, 14.8, 13.0, 11.3, 10.4, 10.8, 12.1, 13.8, 15.3, 16.1, 16.4],
            18: [16.7, 15.9, 14.7, 12.7, 10.9, 10.0, 10.4, 11.8, 13.7, 15.3, 16.2, 16.7],
            20: [16.7, 16.0, 14.5, 12.4, 10.6, 9.6, 10.0, 11.5, 13.5, 15.3, 16.2, 16.8],
            22: [16.9, 16.0, 14.3, 12.0, 10.2, 9.1, 9.6, 11.1, 13.1, 15.2, 16.4, 17.0],
            24: [16.9, 15.9, 14.1, 11.7, 9.8, 8.6, 9.1, 10.7, 13.1, 15.1, 16.5, 17.1],
            26: [17.0, 15.9, 13.9, 11.4, 9.4, 8.1, 8.7, 10.4, 12.8, 15.0, 16.5, 17.3],
            28: [17.1, 15.8, 13.7, 11.1, 9.0, 7.8, 8.3, 10.0, 12.6, 14.9, 16.6, 17.5],
            30: [17.2, 15.7, 13.5, 10.8, 8.5, 7.4, 7.8, 9.6, 12.2, 14.7, 16.7, 17.6]
    }

    @staticmethod
    def month_validation(month):
        """Month validation

        Validates if it was used a valid month

        :param month: The month number
        :type month: int

        :return: Month if monthn is wright
        :rtype: int
        """
        if 1 <= month <= 12:
            return month
        else:
            raise Exception('Mês varia de 1 a 12')

    def get_ho(self, hem, lat, month=1):
        """Get ho

        Function that gets the ho by the hemisphere,
        latitude and number of month.

        :param hem: Hemisphere(south or North)
        :param lat: Place latitude
        :param month: Number of Month

        :type hem: int
        :type lat: float
        :type month: int

        :return: Ho in mm
        :rtype: float
        """
        if hem == 'south':
            try:
                return self.__lat_sul[int(lat)][self.month_validation(month) - 1]
            except Exception as e:
                print("Error: %s" % e)
        elif hem == 'north':
            print(u"There are no values for the north hemisphere")
            return None
        else:
            print("Hemisphere: %s not existent" % hem)
            return False


class ExtraterrestrialIrradiance(Photoperiod):
    """ Extraterrestrial Irradiance

    Extraterrestrial solar irradiance(Ho), expressed in mm
    of equivalent evaporation by day(mm day⁻¹), scientific
    method based on the latitude and day of year

    """

    def ho(self):
        """Ho calculus

        Calculates the Ho in MJ/m²

        :return: Ho in MJ/m
        :rtype: float
        """
        sine_lat = math.sin(math.radians(self.lat))
        sine_sigma = math.sin(math.radians(self.delta()))
        sine_hn = math.sin(math.radians(self.sunrise_time()))
        cosine_lat = math.cos(math.radians(self.lat))
        cosine_delta = math.cos(math.radians(self.delta()))

        return 37.6 * self.relative_distance() * (math.pi / 180.0 * self.sunrise_time() * sine_lat * sine_sigma
                                                  + cosine_lat * cosine_delta * sine_hn)

    def ho_mm(self):
        """Ho in mm calculus

        The Ho in mm . day⁻¹.

        :return Ho in mm . day⁻¹
        :rtype: float
        """
        return self.ho() / 2.45

    def ho_cal_sqaured_cm(self):
        """ Ho in cal cm⁻² day⁻¹

        Computes the Ho in cal . cm⁻² . day⁻¹

        :return: Ho in cal . cm⁻² . day⁻¹
        :rtype: float
        """
        return self.ho() / 0.041868

    def update_date_lat(self, new_date=datetime.now(), lat=None):
        if isinstance(new_date, datetime):
            self.day = new_date
        else:
            raise InputTypeException("new_date must be an valid datetime!")
        if lat is not None:
            if isinstance(lat, float) or isinstance(lat, int) \
                    and -90.00 <= lat <= 90.00:
                self.lat = lat
            else:
                raise InputTypeException("Lat must be a valid latitude of type int or float!")


class Irradiance(Photoperiod):

    def __init__(self, day, lat):
        self.solar_const = 1367.0
        try:
            self.seconds = day.time()
        except:
            raise InputTypeException('wrong datatype in dia, you have used {}, '
                                     'please use a datetime.'.format(type(day).__name__))
        Photoperiod.__init__(self, day, lat)

    @property
    def seconds(self):
        return self.__seconds

    @seconds.setter
    def seconds(self, seconds):
        self.__seconds = seconds.hour * 3600 \
                         + seconds.minute * 60\
                         + seconds.second

    def hour_angle(self):
        hour_angle = (self.seconds - 43200) * 0.00416667
        return round(hour_angle, 2)

    def corrected_solar_const(self):

        return self.solar_const * self.relative_distance()

if __name__ == '__main__':
    qo_jan_piracicaba = {'hem': 'sul', 'lat': 22, 'mes': 1}
    radiacao = RadiationTableMethod()
    print("Piracicaba: ", radiacao.get_ho(**qo_jan_piracicaba))

    dia_teste = datetime(2008, 2, 15, 13, 15)
    dados = {
        "day": dia_teste,
        "lat": -21.23
    }

    radiacaocientifica = ExtraterrestrialIrradiance(**dados)
    print(radiacaocientifica.ho())
    print(radiacaocientifica.ho_cal_sqaured_cm())
    irradiancia = Irradiance(**dados)
    print('irradiancia:')
    print(irradiancia.hour_angle())
