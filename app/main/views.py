#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template

from ..labmet.fao_aquacrop_model.fixes import correcaotemperatura
from . import main
from ..labmet.fao_aquacrop_model.prodbrutafao import PotentialProductivity


@main.route('/')
def index():
    temp_cloudy_days_fix = correcaotemperatura.CTCIIIVerao(24.5).ctn()
    print(temp_cloudy_days_fix)
    temp_clear_days_fix = correcaotemperatura.CTCIIIVerao(24.5).ctc()
    print(temp_clear_days_fix)

    potential_productivity = PotentialProductivity(1001,
                                                   temp_cloudy_days_fix=temp_cloudy_days_fix,
                                                   temp_clear_days_fix=temp_clear_days_fix,
                                                   n_N=0.65)

    print( "Potential productivity: {}".format(potential_productivity.raw_potential_productivity(hectometer_sqr_m=False)))
    print(potential_productivity.__str__())

    return render_template('index.html')