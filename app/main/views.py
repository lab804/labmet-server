#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template

from ..labmet.fao_aquacrop_model.fixes import temperature_fix
from ..labmet.fao_aquacrop_model.fixes.input_variable_fix import *
from . import main
from ..labmet.fao_aquacrop_model.prodfao import PotentialProductivity


@main.route('/')
def index():
    temp_cloudy_days_fix = temperature_fix.SummerTemperatureFixCIII(24.5).clear_days_fix()
    print(temp_cloudy_days_fix)
    temp_clear_days_fix = temperature_fix.SummerTemperatureFixCIII(24.5).cloudy_days_fix()
    print(temp_clear_days_fix)

    n_N = lux_to_n_N(1000)


    potential_productivity = PotentialProductivity(1001,
                                                   temp_cloudy_days_fix=temp_cloudy_days_fix,
                                                   temp_clear_days_fix=temp_clear_days_fix,
                                                   n_N=n_N)

    print( "Potential productivity: {}".format(potential_productivity.raw_potential_productivity(hectometer_sqr_m=False)))
    print(potential_productivity.__str__())

    return render_template('index.html')