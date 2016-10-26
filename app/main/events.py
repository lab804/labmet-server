#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from datetime import datetime, timedelta
from .. import socketio

from config import Config
from notification import Notification

from labmet import ExtraterrestrialIrradiance, \
    ThornthwaiteETo, ThornthwaiteWaterBalance, ObtainableProductivity, \
    SummerTemperatureFixCIII, PotentialProductivity, BreathingFix, \
    HarvestedPartFix, LeafAreaIndexFix, lux_to_n_N, soil_moisture_to_mm

notification = Notification(Config.NOTIFICATIONKEY)  # o.0

eto_potato = 0.8
awc_potato = 35
soil_moisture = 35
precipitation = 0
ky_potato = 1.1
avg_year_temp = 19
radiation_data = {
        "day": datetime.now(),
        "lat": 51.5044968
    }
extra_radiation = ExtraterrestrialIrradiance(**radiation_data)
eto = ThornthwaiteETo(avg_year_temp,
                      extra_radiation.photoperiod(),
                      1,
                      avg_year_temp).eto_day() * eto_potato
real_et = eto

obtainable_productivity = ObtainableProductivity(ky=ky_potato)

NIGHT = 5  # Hour (supposedly)
SECONDS_DELAY = 10 # Delay send push just example massive.
DELAY = datetime.now() + timedelta(seconds=SECONDS_DELAY)

CULTURE = {
    'POTATO': {
        'BEST_PERFOMACE': {
            'ILLUMINACE': 3,
            'TEMPMAX': 30.5,
            'TEMPMIN': 9.3,
        },
        'MSGS': {
            'LESS_ILLUMINACE': 'missing light'
        }
    }
}


def on_mesage(mosq, obj, msg):
    global ERROR  # crazy o.0
    global DELAY
    global obtainable_productivity
    global extra_radiation
    global soil_moisture
    global precipitation
    global eto
    global awc_potato
    global real_et

    n_days = 130
    peak_l_a_index = 3
    json_msg = json.loads(msg.payload)
    json_msg['id'] = 123
    json_msg['status'] = 1

    radiation_data = {
        "day": datetime.now(),
        "lat": 51.5044968
    }
    extra_radiation = ExtraterrestrialIrradiance(**radiation_data)

    temp_cloudy_days_fix = SummerTemperatureFixCIII(temperature=json_msg["ds18b20_temp"]).clear_days_fix()
    temp_clear_days_fix = SummerTemperatureFixCIII(temperature=json_msg["ds18b20_temp"]).cloudy_days_fix()

    n_N = lux_to_n_N(json_msg["bh1750_illuminance"])
	
    potential_productivity = PotentialProductivity(extra_radiation.ho_cal_sqaured_cm(),
                                                   temp_cloudy_days_fix=temp_cloudy_days_fix,
                                                   temp_clear_days_fix=temp_clear_days_fix,
                                                   n_N=n_N)

    breath_fix = BreathingFix(temperature=json_msg["ds18b20_temp"]).breathing_fix()
    harvest_fix = HarvestedPartFix("potato").harvested_part_fix()["average"]
    leaf_area_fix = LeafAreaIndexFix(peak_l_a_index).leaf_area_index_fix()

    json_msg["potential_productivity"] = potential_productivity.potential_productivity(leaf_area_fix,
                                                                                       breath_fix,
                                                                                       harvest_fix,
                                                                                       n_days,
                                                                                       hectometer_sqr_m=True)
    json_msg["real_productivity"] = \
        obtainable_productivity.obtainable_productivity(etc=real_et,
                                                        eto=eto,
                                                        potential_productivity=json_msg["potential_productivity"])

    read_soil_moisture = soil_moisture_to_mm(json_msg['analog_soil_moisture'], awc_potato)
    variation = read_soil_moisture - soil_moisture

    if read_soil_moisture > eto:
        real_et = eto
        if variation >= awc_potato:
            precipitation = awc_potato
        else:
            precipitation = variation
    else:
        precipitation = 0
        real_et = read_soil_moisture 

    soil_moisture = read_soil_moisture
    radiation_data["day"] = datetime.now()
    eto = ThornthwaiteETo(avg_year_temp,
                          extra_radiation.photoperiod(),
                          30,
                          avg_year_temp).eto_day() * eto_potato

    
    json_msg["precipitation"] = precipitation
    json_msg["eto"] = eto
    json_msg["etc"] = real_et
	   
    socketio.emit('my response', {'topic': msg.topic, 'payload': json_msg},
                  namespace='/weather_data')

    if json_msg['bh1750_illuminance'] < CULTURE['POTATO']['BEST_PERFOMACE']['ILLUMINACE']:
        # is night?
        now = datetime.now()

        if now.hour > NIGHT and now > DELAY:
            msg = CULTURE['POTATO']['MSGS']['LESS_ILLUMINACE']
            notification.send_push_all(msg)
            ERROR = True
            DELAY = now + timedelta(seconds=SECONDS_DELAY)
