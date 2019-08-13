#!/usr/bin/env python3

import json
import os
import sys
import time

import ltr559
import paho.mqtt.client as mqtt

from bme280 import BME280
from pms5003 import PMS5003
# MICS-6814 Sensor
from enviroplus import gas as GAS
from numpy import interp

INTERVAL = int(os.getenv('INTERVAL', '300'))
DEVICE_NAME = os.getenv('DEVICE_NAME', 'AirTower')

MQTT_SERVER = os.getenv('MQTT_SERVER', 'localhost')
MQTT_PORT = int(os.getenv('MQTT_PORT', '1883'))
MQTT_BASE_TOPIC = os.getenv('MQTT_BASE_TOPIC', 'homeassistant')
MQTT_KEEPALIVE = int(os.getenv('MQTT_KEEPALIVE', '60'))

METRICS = {'temperature': {'name': 'Temperature', 'unit': 'C',
                           'class': 'temperature'},
           'pressure': {'name': 'Pressure', 'unit': 'hPa',
                        'class': 'pressure'},
           'humidity': {'name': 'humidity', 'unit': '%',
                        'class': 'humidity'},
           'light': {'name': 'light', 'unit': 'Lux', 'class': 'illuminance'},
           'oxidising': {'name': 'Oxidising gases', 'unit': 'ppm'},
           'reducing': {'name': 'Reducing gases', 'unit': 'ppm'},
           'nh3': {'name': 'Ammonia', 'unit': 'ppm'},
           'pm1': {'name': 'PM 1', 'unit': 'ug/m3'},
           'pm25': {'name': 'PM 2.5', 'unit': 'ug/m3'},
           'pm10': {'name': 'PM 10', 'unit': 'ug/m3'}}


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
    PM_SENSOR.enable()
    # Give some time for the sensor to settle down
    time.sleep(5)
    data = PM_SENSOR.read()
    PM_SENSOR.disable()
    return data


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
    '''Prime the sensors. The initial reading are ignored because they are
    not quite right yet.'''
    get_gas_data()
    ltr559.get_lux()
    get_particulate_data()


try:
    print("Initialising")
    init_hw()
    # MQTT Connection
    print("Connecting to MQTT broker")
    mqtt_client = mqtt.Client()
    mqtt_client.connect(MQTT_SERVER,
                        MQTT_PORT,
                        MQTT_KEEPALIVE)
    # Declaring sensors for home assistant auto discovery
    print("Announcing devices to Home Assistant")
    base_path = "{}/sensor/{}".format(MQTT_BASE_TOPIC, DEVICE_NAME.lower())
    state_path = "{}/state".format(base_path)
    for name, metric in METRICS.items():
        payload = {'name': "{} {}".format(DEVICE_NAME, metric['name']),
                   'unit_of_measurement': metric['unit'],
                   'state_topic': state_path,
                   'value_template': "{{{{ value_json.{} }}}}".format(name)}
        if 'class' in metric:
            payload['device_class'] = metric['class']
        config_path = "{}/{}_{}/config".format(base_path,
                                               DEVICE_NAME.lower(),
                                               name)
        print(payload)
        mqtt_client.publish(config_path, json.dumps(payload), 1, True)
    print("Startup finished")
    # Main loop
    while True:
        print(time.ctime())
        data = get_all_metrics()
        payload = {}
        for name in METRICS.keys():
            payload[name] = round(data[name], 2)
        print(payload)
        mqtt_client.publish(state_path, json.dumps(payload))
        time.sleep(INTERVAL)
except KeyboardInterrupt:
    sys.exit(0)
