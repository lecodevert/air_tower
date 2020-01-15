#!/usr/bin/env python3
'''Main AirTower file'''

import json
import os
import sys
import time

from numpy import interp
import ltr559
import paho.mqtt.client as mqtt
from bme280 import BME280
from modules.display import e_paper
from modules import gas as GAS

from pms5003 import PMS5003

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

import logging


BUS = SMBus(1)

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
           'humidity': {'name': 'Humidity', 'unit': '%',
                        'class': 'humidity'},
           'light': {'name': 'light', 'unit': 'Lux', 'class': 'illuminance'},
           'oxidising': {'name': 'Oxidising gases', 'unit': 'ppm'},
           'reducing': {'name': 'Reducing gases', 'unit': 'ppm'},
           'nh3': {'name': 'Ammonia', 'unit': 'ppm'},
           'pm1': {'name': 'PM 1', 'unit': 'ug/m3'},
           'pm25': {'name': 'PM 2.5', 'unit': 'ug/m3'},
           'pm10': {'name': 'PM 10', 'unit': 'ug/m3'}}


def get_temperature(tph_sensor):
    '''Get temperature from sensor.'''
    return tph_sensor.get_temperature()


def get_humidity(tph_sensor):
    '''Get ambient humidity from sensor.'''
    return tph_sensor.get_humidity()


def get_pressure(tph_sensor):
    '''Get atmospheric pressure from sensor.'''
    return tph_sensor.get_pressure()


def get_light():
    '''Get light level from sensor.'''
    return ltr559.get_lux()


def get_oxidising(gas_data):
    '''Get oxidising gas concentration from sensor data.'''
    return interp(gas_data.oxidising / 1000, [0.8, 20], [0.05, 10])


def get_reducing(gas_data):
    '''Get reducing gas concentration from sensor data.'''
    return interp(gas_data.reducing / 1000, [100, 1500], [1, 1000])


def get_nh3(gas_data):
    '''Get ammonia gas concentration from sensor data.'''
    return interp(gas_data.nh3 / 1000, [10, 1500], [1, 300])


def get_pm1(pm_data):
    '''Get 1 micron particulate level from sensor data.'''
    return pm_data.pm_ug_per_m3(1.0)


def get_pm25(pm_data):
    '''Get 2.5 microns particulate level from sensor data.'''
    return pm_data.pm_ug_per_m3(2.5)


def get_pm10(pm_data):
    '''Get 10 microns particulate level from sensor data.'''
    return pm_data.pm_ug_per_m3(10)


def get_particulate_data(pm_sensor):
    '''Get aggregate particulate data from sensor.'''
    pm_sensor.enable()
    # Give some time for the sensor to settle down
    time.sleep(5)
    pm_data = pm_sensor.read()
    pm_sensor.disable()
    return pm_data


def get_all_metrics():
    '''Get all data from sensors.'''
    gas_data = GAS.read_all()
    pm_data = get_particulate_data(PMS5003())
    tph_sensor = BME280(i2c_dev=BUS)
    tph_sensor.setup(mode="forced")

    all_data = {}
    for metric in METRICS:
        params = []
        if metric in ['oxidising', 'reducing', 'nh3']:
            params = [gas_data]
        elif metric in ['pm1', 'pm25', 'pm10']:
            params = [pm_data]
        elif metric in ['temperature', 'pressure', 'humidity']:
            params = [tph_sensor]
        all_data[metric] = globals()["get_{}".format(metric)](*params)

    del gas_data
    return all_data


def on_connect(_client, _userdata, _flags, result_code):
    '''Used for debugging mqtt connection errors.'''
    info = {0: "Connected",
            1: "Connection refused – incorrect protocol version",
            2: "Connection refused – invalid client identifier",
            3: "Connection refused – server unavailable",
            4: "Connection refused – bad username or password",
            5: "Connection refused – not authorised"}
    print(info[result_code])


def on_disconnect(_client, _userdata, _rc):
    '''Indicates when connection to mqtt server has been closed.'''
    print("Client Got Disconnected")


try:
    print("Initialising")
    EPAPER = e_paper.Epaper()
    EPAPER.display_network_info()
    # MQTT Connection
    print("Connecting to MQTT broker")
    MQTT = mqtt.Client()
    MQTT.on_connect = on_connect
    MQTT.on_disconnect = on_disconnect
    MQTT.loop_start()
    MQTT.connect(MQTT_SERVER,
                 MQTT_PORT,
                 MQTT_KEEPALIVE)
    # Declaring sensors for home assistant auto discovery
    print("Announcing devices to Home Assistant")
    BASE_PATH = "{}/sensor/{}".format(MQTT_BASE_TOPIC, DEVICE_NAME.lower())
    STATE_PATH = "{}/state".format(BASE_PATH)
    for name, metric_params in METRICS.items():
        payload = {'name': "{} {}".format(DEVICE_NAME, metric_params['name']),
                   'unit_of_measurement': metric_params['unit'],
                   'state_topic': STATE_PATH,
                   'value_template': "{{{{ value_json.{} }}}}".format(name)}
        if 'class' in metric_params:
            payload['device_class'] = metric_params['class']
        config_path = "{}/{}_{}/config".format(BASE_PATH,
                                               DEVICE_NAME.lower(),
                                               name)
        print(payload)
        MQTT.publish(config_path, json.dumps(payload), 1, True)
    print("Startup finished")
    # Main loop
    while True:
        print(time.ctime())
        DATA = get_all_metrics()
        PAYLOAD = {name: round(DATA[name], 2) for name in METRICS}
        print(PAYLOAD)
        MQTT.publish(STATE_PATH, json.dumps(PAYLOAD))
        EPAPER.display_all_data(PAYLOAD['temperature'], bg='all_data.bmp')
        EPAPER.sleep()
        time.sleep(INTERVAL - 2)
except KeyboardInterrupt:
    sys.exit(0)
