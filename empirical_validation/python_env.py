from flask import Flask, jsonify, request
from datetime import datetime

class Observation:
    def __init__(self, value: float, timestamp: datetime, extra_info = None):
        self.value = value
        self.timestamp = timestamp
        self.extra_info = extra_info

    def to_dict(self):
        return {
            'value': self.value,
            'timestamp': self.timestamp,
            'extra_info': self.extra_info
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
    
    def get_last_observation(self):
        if self.observations:
            return self.observations[-1].to_dict()
        return None

    def to_dict(self):
        return {
            'name': self.name,
            'measure': self.measure
        }
class Visitor:
    def __init__(self, name: str, lastname: str, role: str, gender: str, limitations =[]):
        self.visitor_public_data =[]
        self.visitor_private_data =[]
        self.visitor_public_data.append(PublicData('name', name))
        self.visitor_public_data.append(PublicData('lastname', lastname))
        self.visitor_public_data.append(PublicData('role', role))
        self.visitor_private_data.append(PrivateData('gender', gender))

        for limitation in limitations:
            self.visitor_private_data.append(PrivateData(limitation.name, limitation.value))

        self.member_of_privacy_comunity = None
        self.eval_if_member_of_privacy_comunity(role)

    def eval_if_member_of_privacy_comunity(self, role):
        if role == 'admin':
            self.member_of_privacy_comunity = True
        self.member_of_privacy_comunity = False

    def to_dict(self):
        return {
            'publicData':  [data.to_dict() for data in self.visitor_public_data],
        }

class PublicData:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def to_dict(self):
        return {
            'name': self.name,
            'value': self.value
        }
class PrivateData:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def to_dict(self):
        return {
            'name': self.name,
            'value': self.value
        }
    
class Paint:
    def __init__(self, title: PublicData, author: PublicData, technique: PublicData, historicalValue: PrivateData, monetaryValue: PrivateData):
        self.title = title
        self.author = author
        self.technique = technique
        self.historicalValue = historicalValue
        self.monetaryValue = monetaryValue

    def to_dict(self):
        return {
            'title': self.title.to_dict(),
            'author': self.author.to_dict(),
            'technique': self.technique.to_dict(),
            'historicalValue': self.historicalValue.to_dict(),
            'monetaryValue': self.monetaryValue.to_dict()
        }
class PythonEnvironment:
    def __init__(self, sensors = [], visitors = [], arts = []):
        self.sensors =  sensors
        self.visitors = visitors
        self.arts = arts

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
        extra_info = data.get('extra_info')
        timestamp_now = datetime.now()
        formatted_date = timestamp_now.strftime("%d-%m-%Y %H:%M:%S")

        sensor = self.get_sensor_by_name(sensor_name)
        if sensor:
            sensor.add_observation(Observation(value, formatted_date, extra_info=extra_info))
            return 'Observation received', 201
        return 'Sensor not found', 404
    
    def get_last_observations(self):
        last_observations = []
        for sensor in self.sensors:
            last_observation = sensor.get_last_observation()
            last_observations.append({
                'sensor': sensor.name,
                'last_observation': last_observation
            })
        return jsonify(last_observations)
    
    def add_visitor(self, data):
        role = data.get('role')
        name = data.get('name')
        lastname = data.get('lastname')
        gender = data.get('gender')
        valid_types = ['visitante', 'admin', 'personal de restauracion'] #TODO: move to constants
        if role not in valid_types:
            return f"Tipo must be one of {valid_types}", 400
        new_visitor = Visitor(name, lastname, role, gender)
        self.visitors.append(new_visitor)
        return 'visitor added', 201

    def count_visitors(self):
        return jsonify(len(self.visitors))
    
    def list_visitors(self):
        return jsonify([visitor.to_dict() for visitor in self.visitors])

    def add_paint(self, data):
        title = PublicData(name="Title", value="Starry Night")
        author = PublicData(name="Author", value="Vincent van Gogh")
        technique = PublicData(name="Technique", value="Oil on canvas")
        historical_value = PrivateData(name="Historical Value", value="High")
        monetary_value = PrivateData(name="Monetary Value", value="Priceless")

        new_paint = Paint(title, author, technique, historical_value, monetary_value)
        self.arts.append(new_paint)
        return 'paint added', 201
