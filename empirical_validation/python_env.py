from flask import Flask, jsonify, request
from datetime import datetime

class Observation:
    def __init__(self, value: float, timestamp: datetime):
        self.value = value
        self.timestamp = timestamp

    def to_dict(self):
        return {
            'value': self.value,
            'timestamp': self.timestamp
        }

class Sensor:
    def __init__(self, name: str, measure: str):
        self.name = name
        self.measure = measure
        self.observations = []

    def add_observation(self, observation: Observation):
        self.observations.append(observation)

    def get_observations(self):
        return jsonify([obs.to_dict() for obs in self.observations])

    def to_dict(self):
        return {
            'name': self.name,
            'measure': self.measure
        }

class PythonEnvironment:
    def __init__(self, sensors = [], visitors = []):
        self.sensors =  sensors
        self.visitors = visitors

    def sensor_exists(self, sensors, sensor_to_check):
        for sensor in sensors:
            if sensor.name == sensor_to_check.name and sensor.measure == sensor_to_check.measure:
                return True
        return False
    def get_sensor_by_name(self, sensor_name):
        for sensor in self.sensors:
            if sensor.name == sensor_name:
                return sensor
        return None

    def get_sensors(self):
        return jsonify([sensor.to_dict() for sensor in self.sensors])
    
    def get_sensors_names(self):
        return jsonify([sensor.name for sensor in self.sensors])

    def add_sensor(self, data):
        req_name = data.get('name')
        req_measure = data.get('measure')
        new_sensor = Sensor(name=req_name, measure=req_measure)
        if self.sensor_exists(self.sensors, new_sensor):
            return 'Sensor already exists', 400
        self.sensors.append(new_sensor)
        return 'sensor added', 201
    
    def get_sensor_observation(self, sensor_name):
        sensor = self.get_sensor_by_name(sensor_name)
        if sensor:
           return sensor.get_observations()
        return 'Sensor not found', 404
    
    def add_observation(self, data):
        sensor_name = data.get('sensor')
        value = data.get('value')
        timestamp_now = datetime.now()
        formatted_date = timestamp_now.strftime("%d-%m-%Y %H:%M:%S")

        sensor = self.get_sensor_by_name(sensor_name)
        if sensor:
            sensor.add_observation(Observation(value, formatted_date))
            return 'Observation received', 201
        return 'Sensor not found', 404