from flask import Flask, jsonify, request


class Sensor:
    def __init__(self, name: str, measure: str):
        self.name = name
        self.measure = measure

    def to_dict(self):
        return {
            'name': self.name,
            'measure': self.measure
        }

class PythonEnvironment:
    def __init__(self, sensors = [], observations = [], visitors = []): # TODO: define sensors as a list of Sensors and same for properties
        self.sensors =  sensors
        self.observations = observations
        self.visitors = visitors

    def sensor_exists(self, sensors, sensor_to_check):
        for sensor in sensors:
            if sensor.name == sensor_to_check.name and sensor.measure == sensor_to_check.measure:
                return True
        return False

    def get_sensors(self):
        return jsonify([sensor.to_dict() for sensor in self.sensors])

    def add_sensor(self, req_name, req_measure):
        new_sensor = Sensor(name=req_name, measure=req_measure)
        if self.sensor_exists(self.sensors, new_sensor):
            return 'Sensor already exists', 400
        self.sensors.append(new_sensor)
        return 'sensor added', 201