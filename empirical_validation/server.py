from flask import Flask, jsonify, request
import rdflib
from rdflib import Graph, Literal, BNode, Namespace, RDF, XSD, OWL,URIRef


app = Flask(__name__)


# Define namespaces
sosa = Namespace('https://www.w3.org/ns/sosa/')
seas = Namespace('https://w3id.org/seas/')
xsd = Namespace('http://www.w3.org/2001/XMLSchema#')
ioto = Namespace("https://github.com/Alex23013/Ioto-Semantic-for-IoT-Environments/blob/main/iot_ontologies/ioto-protege.ttl/")

# Constants
g = Graph()
sensors = []
observations = []

measure_to_property = {
    'temperature': seas.temperature,
    'humidity': seas.humidity,
    'pressure': seas.pressure,
    # Add more mappings as needed
}

class Sensor:
    def __init__(self, name: str, measure: str):
        self.name = name
        self.measure = measure

    def to_dict(self):
        return {
            'name': self.name,
            'measure': self.measure
        }

def sensor_exists(sensors, sensor_to_check):
    for sensor in sensors:
        if sensor.name == sensor_to_check.name and sensor.measure == sensor_to_check.measure:
            return True
    return False

@app.route('/sensors')
def get_sensors():
    return jsonify([sensor.to_dict() for sensor in sensors])


@app.route('/sensors', methods=['POST'])
def add_sensor():
    data = request.get_json()
    name = data.get('name')
    measure = data.get('measure')
    if not name or not measure:
        return 'Invalid sensor data', 400
    new_sensor = Sensor(name=name, measure=measure)
    if sensor_exists(sensors, new_sensor):
        return 'Sensor already exists', 400
    sensors.append(new_sensor)
    
    new_sensor_uri = ioto[name]
    g.add((new_sensor_uri, RDF.type, sosa.Sensor))
    g.add((new_sensor_uri, sosa.hasName, Literal(new_sensor.name, datatype=XSD.string))) 
    observed_property = measure_to_property.get(measure.lower())
    if observed_property:
        g.add((new_sensor_uri, sosa.observes, observed_property))
    else:
        return 'Invalid measure', 400
    
    return 'sensor added', 201

@app.route('/observations')
def get_observations():
    #TODO: Implment observation to be an object like sensor
    return jsonify(observations)

@app.route('/observations', methods=['POST'])
def add_observation():
    data = request.get_json()
    sensor_name = data.get('name')
    value = data.get('value')
    if not sensor_name or not value:
        return 'Invalid observation data', 400

    found_sensor = next((sensor for sensor in sensors if sensor.name == sensor_name), None)
    if not found_sensor:
        return 'Sensor not found', 404

    # Get the observed property dynamically based on the sensor's measure
    observed_property = measure_to_property.get(found_sensor.measure.lower())
    if not observed_property:
        return 'Invalid measure', 400
    
    num_obs = len(observations)
    observation = ioto[found_sensor.name + '_observation_'+str(num_obs)]
    g.add((observation, RDF.type, sosa.Observation))
    g.add((observation, sosa.madeBySensor, URIRef(ioto[found_sensor.name])))
    g.add((observation, sosa.observedProperty, observed_property))
    g.add((observation, sosa.hasResult, Literal(value, datatype=XSD.float)))

    return 'observation received', 201

@app.route("/")
def welcome_message():
    return "Hello, from smart building!"


@app.route('/turtle_ontology')
def get_ontology_format_turtle():
    format = request.args.get('format', 'turtle')
    valid_formats = ['turtle', 'xml', 'n3', 'nt', 'json-ld']
    if format not in valid_formats:
        return 'Invalid format', 400
    return g.serialize(format=format)

# create a method that analyse the observations and get high level info
# create a method that initiate the building instance (set ethic mode and info about data controllers)
# we ca make form to fill in the data



if __name__ == '__main__':
    app.run(port=5000)