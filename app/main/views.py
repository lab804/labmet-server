#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template

from labmet.fao_aquacrop_model import lux_to_n_N, soil_moisture_to_mm, BreathingFix, \
    HarvestedPartFix, LeafAreaIndexFix, SummerTemperatureFixCIII
from labmet.radiation import ExtraterrestrialIrradiance
from labmet.evapotranspiration import ThornthwaiteETo

from . import main
from labmet import PotentialProductivity, ObtainableProductivity, ThornthwaiteWaterBalance
from datetime import datetime


@main.route('/')
def index():
    temperature = 13
    n_N = lux_to_n_N(1000)
    radiation_data = {
        "day": datetime.now(),
        "lat": 51.5044968
    }
    awc_potato = 35
    humidity = 30
    hum = soil_moisture_to_mm(humidity, 35)
    ky = 1.1
    avg_year_temp = 19
    extra_radiation = ExtraterrestrialIrradiance(**radiation_data)
    eto = ThornthwaiteETo(temperature, extra_radiation.photoperiod(), 1, avg_year_temp).eto_day()
    eto = 0.8 * eto
    print "eto", eto

    t_wb = ThornthwaiteWaterBalance(awc=awc_potato, soil_water_moisture=hum)

    wb = t_wb.thornthwaite_water_balance(precipitation=0, eto=eto)
    print wb
    etc = wb["real_et"]
    print "evapo cultura", etc

    temp_cloudy_days_fix = SummerTemperatureFixCIII(temperature=temperature).clear_days_fix()
    temp_clear_days_fix = SummerTemperatureFixCIII(temperature=temperature).cloudy_days_fix()

    potential_productivity = PotentialProductivity(extra_radiation.ho_cal_sqaured_cm(),
                                                   temp_cloudy_days_fix=temp_cloudy_days_fix,
                                                   temp_clear_days_fix=temp_clear_days_fix,
                                                   n_N=n_N)

    obtainable_productivity = ObtainableProductivity(ky)

    breath_fix = BreathingFix(temperature=temperature).breathing_fix()
    harvest_fix = HarvestedPartFix("potato").harvested_part_fix()["average"]
    leaf_area_fix = LeafAreaIndexFix(3).leaf_area_index_fix()
    n_days = 130

    pot_productivity = potential_productivity.potential_productivity(leaf_area_fix,
                                                                     breath_fix,
                                                                     harvest_fix,
                                                                     n_cycle_days=n_days,
                                                                     hectometer_sqr_m=True)

    print ("Brute Potential productivity: {}".format(potential_productivity.raw_potential_productivity(n_cycle_days=n_days, hectometer_sqr_m=True)))

    print "Potential productivity:", pot_productivity

    print "Real productivity: ", obtainable_productivity.obtainable_productivity(etc, eto, pot_productivity)

    return render_template('index.html')