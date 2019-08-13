#!/usr/bin/env python3

import ltr559
import RPi.GPIO as GPIO
import time

from bme280 import BME280
from pms5003 import PMS5003
# MICS-6814 Sensor
from enviroplus import gas as GAS


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
    # FIXME: convert kOhms to ppm value
    return gas_data.oxidising / 1000


def get_reducing(gas_data):
    # FIXME: convert kOhms to ppm value
    return gas_data.reducing / 1000


def get_nh3(gas_data):
    # FIXME: convert kOhms to ppm value
    return gas_data.nh3 / 1000


def get_pm1(pm_data):
    return pm_data.pm_ug_per_m3(1.0)


def get_pm25(pm_data):
    return pm_data.pm_ug_per_m3(2.5)


def get_pm10(pm_data):
    return pm_data.pm_ug_per_m3(10)


def get_gas_data():
    return GAS.read_all()


def get_particulate_data():
    try:
        return PM_SENSOR.read()
    except PMS5003.ReadTimeoutError:
        return PMS5003()


def get_all_metrics():
    # Start by powering on the Particulate sensor
    GPIO.output(22, True)
    gas_data = get_gas_data()
    for i in range(2):
        pm_data = get_particulate_data()
        time.sleep(1)

    data = {}
    for name, _metric in METRICS.items():
        if name in ['oxidising', 'reducing', 'nh3']:
            data[name] = globals()["get_{}".format(name)](gas_data)
        elif name in ['pm1', 'pm25', 'pm10']:
            data[name] = globals()["get_{}".format(name)](pm_data)
        else:
            data[name] = globals()["get_{}".format(name)]()
    # shutdown PM sensor
    GPIO.output(22, False)
    return data


def init_hw():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.OUT)

init_hw()
data = get_all_metrics()

for name, metric in METRICS.items():
    metric['value'] = data[name]
    print("{name}: {value}{unit}".format(**metric))
