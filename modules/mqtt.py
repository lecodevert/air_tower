'''MQTT related features.'''
import json
import logging
import paho.mqtt.client as mqtt_client


def on_connect(_client, _userdata, _flags, result_code):
    '''Used for debugging mqtt connection errors.'''
    info = {0: "Connected",
            1: "Connection refused – incorrect protocol version",
            2: "Connection refused – invalid client identifier",
            3: "Connection refused – server unavailable",
            4: "Connection refused – bad username or password",
            5: "Connection refused – not authorised"}
    if result_code == 0:
        logging.info(info[result_code])
    else:
        logging.error(info[result_code])


def on_disconnect(_client, _userdata, _rc):
    '''Indicates when connection to mqtt server has been closed.'''
    logging.info("Client Got Disconnected")


class Mqtt:
    '''Wrapper for MQTT features.'''

    # pylint: disable=too-many-arguments
    def __init__(self, server='localhost', port='1883',
                 base_topic='homeassistant', keepalive='60',
                 device_name='AirTower'):
        '''MQTT Connection and configuration.'''
        logging.info("Connecting to MQTT broker")
        self.client = mqtt_client.Client()
        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.loop_start()
        self.client.connect(server, port, keepalive)
        self.device_name = device_name
        self.base_topic = base_topic
        self.base_path = "{}/sensor/{}".format(base_topic, device_name.lower())
        self.state_path = "{}/state".format(self.base_path)

    def homeassistant_config(self, metrics):
        '''Declaring sensors for home assistant auto discovery.'''
        logging.info("Announcing devices to Home Assistant")
        for name, metric_params in metrics.items():
            payload = {'name': "{} {}".format(self.device_name,
                                              metric_params['name']),
                       'unit_of_measurement': metric_params['unit'],
                       'state_topic': self.state_path,
                       'value_template':
                       "{{{{ value_json.{} }}}}".format(name)}
            if 'class' in metric_params:
                payload['device_class'] = metric_params['class']
            config_path = "{}/{}_{}/config".format(self.base_path,
                                                   self.device_name.lower(),
                                                   name)
            logging.debug(payload)
            self.client.publish(config_path, json.dumps(payload), 1, True)

    def publish_metrics(self, data, metrics):
        '''Publish measurements to mqtt broker.'''
        payload = {name: round(data[name]['value'], 2) for name in metrics}
        logging.debug(payload)
        self.client.publish(self.state_path, json.dumps(payload))
