#!/usr/bin/env python3

import ltr559
import sys
import time

from bme280 import BME280
from pms5003 import PMS5003
# MICS-6814 Sensor
from enviroplus import gas as GAS
from numpy import interp

INTERVAL = 5

METRICS = {'temperature': {'name': 'Temperature', 'unit': '°C',
                           'class': 'temerature'},
           'pressure': {'name': 'Barometric pressure', 'unit': 'hPa',
                        'class': 'pressure'},
           'humidity': {'name': 'humidity', 'unit': '%',
                        'class': 'humidity'},
           'light': {'name': 'light', 'unit': 'Lux', 'class': 'illuminance'},
           'oxidising': {'name': 'Oxidising gases', 'unit': 'ppm'},
           'reducing': {'name': 'Reducing gases', 'unit': 'ppm'},
           'nh3': {'name': 'Ammonia', 'unit': 'ppm'},
           'pm1': {'name': '1 micrometers particles', 'unit': 'ug/m3'},
           'pm25': {'name': '2.5 micrometers particles', 'unit': 'ug/m3'},
           'pm10': {'name': '10 micrometers particles', 'unit': 'ug/m3'}
           }


# BME280 temperature/pressure/humidity sensor
TPH_SENSOR = BME280()

# PMS5003 particulate sensor
PM_SENSOR = PMS5003()

PMS5003_ENABLE_PIN = 22

def get_temperature():
    return TPH_SENSOR.get_temperature()


def get_humidity():
    return TPH_SENSOR.get_humidity()


def get_pressure():
    return TPH_SENSOR.get_pressure()


def get_light():
    return ltr559.get_lux()


def get_oxidising(gas_data):
    return interp(gas_data.oxidising / 1000, [0.8, 20], [0.05, 10])


def get_reducing(gas_data):
    return interp(gas_data.reducing / 1000, [100, 1500], [1, 1000])


def get_nh3(gas_data):
    return interp(gas_data.nh3 / 1000, [10, 1500], [1, 300])


def get_pm1(pm_data):
    return pm_data.pm_ug_per_m3(1.0)


def get_pm25(pm_data):
    return pm_data.pm_ug_per_m3(2.5)


def get_pm10(pm_data):
    return pm_data.pm_ug_per_m3(10)


def get_gas_data():
    return GAS.read_all()


def get_particulate_data():
    max_retries = 10
    retries = 0
    while True:
        try:
            return PM_SENSOR.read()
        except PMS5003.ReadTimeoutError:
            if retries > max_retries:
                break
            retries = retries + 1
            print("Retrying...")
            continue


def get_all_metrics():
    gas_data = get_gas_data()
    pm_data = get_particulate_data()

    data = {}
    for name in METRICS.keys():
        params = []
        if name in ['oxidising', 'reducing', 'nh3']:
            params = [gas_data]
        elif name in ['pm1', 'pm25', 'pm10']:
            params = [pm_data]
        data[name] = globals()["get_{}".format(name)](*params)
    return data


def init_hw():
    get_gas_data()
    ltr559.get_lux()
    get_particulate_data()


init_hw()
try:
    while True:
        data = get_all_metrics()

        for name, metric in METRICS.items():
            metric['value'] = data[name]
            print("{name}: {value}{unit}".format(**metric))
        print('---------------------------------------------------------')
        time.sleep(INTERVAL)
except KeyboardInterrupt:
    sys.exit(0)
