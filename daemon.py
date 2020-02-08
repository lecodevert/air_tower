#!/usr/bin/env python3
'''Main AirTower file'''

import os
import sys
import time
import logging
from datetime import datetime

import ltr559
from numpy import interp
from bme280 import BME280
from influxdb import InfluxDBClient
from modules import e_paper
from modules import gas as GAS
from modules import mqtt
from pms5003 import PMS5003

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s - %(message)s')

BUS = SMBus(1)
INFLUXDB = InfluxDBClient()

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
           'oxidising': {'name': 'NO2', 'unit': 'ppm'},
           'reducing': {'name': 'CO', 'unit': 'ppm'},
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
    tph_sensor.setup(mode='forced')

    all_data = {}
    for metric in METRICS:
        params = []
        if metric in ['oxidising', 'reducing', 'nh3']:
            params = [gas_data]
        elif metric in ['pm1', 'pm25', 'pm10']:
            params = [pm_data]
        elif metric in ['temperature', 'pressure', 'humidity']:
            params = [tph_sensor]
        all_data[metric] = METRICS[metric]
        all_data[metric]['value'] = globals()["get_{}".format(metric)](*params)

    del gas_data
    return all_data


def generate_influxdb_points(data):
    '''Generate the data structure for feeding influxdb measurements.'''
    generated = []
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    for value in data.values():
        generated.append({"measurement": value['name'],
                          "time": now,
                          "fields": {
                              "value": float(round(value['value'], 2)),
                              "unit": value['unit']}
                          })
    return generated


try:
    logging.info("Initialising")
    EPAPER = e_paper.Epaper()
    EPAPER.display_network_info(background='init.bmp')
    INFLUXDB.create_database('air_quality')
    INFLUXDB.switch_database('air_quality')
    MQTT = mqtt.Mqtt(server=MQTT_SERVER,
                     port=MQTT_PORT,
                     base_topic=MQTT_BASE_TOPIC,
                     keepalive=MQTT_KEEPALIVE,
                     device_name=DEVICE_NAME)
    MQTT.homeassistant_config(METRICS)
    logging.info("Startup finished")

    # Main loop
    while True:
        DATA = get_all_metrics()
        MQTT.publish_metrics(DATA, METRICS)
        EPAPER.display_all_data(DATA, background='all_data.bmp')
        INFLUXDB.write_points(generate_influxdb_points(DATA))
        time.sleep(INTERVAL - 7)
except KeyboardInterrupt:
    sys.exit(0)
