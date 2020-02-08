from influxdb import InfluxDBClient
from datetime import datetime

class InfluxDB:

    def __init__(self):
        '''Init connection and database.'''
        #TODO: add connection parameters and configurable database name
        self.influxdb = InfluxDBClient()
        self.influxdb.create_database('air_quality')
        self.influxdb.switch_database('air_quality')

    @staticmethod
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

    def publish_metrics(self, data):
        self.influxdb.write_points(self.generate_influxdb_points(data))
