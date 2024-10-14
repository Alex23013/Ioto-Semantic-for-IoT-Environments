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
measure_to_property = {
    'temperature': seas.temperature,
    'humidity': seas.humidity,
    'pressure': seas.pressure,
    # Add more mappings as needed
}
valid_formats = ['turtle', 'xml', 'n3', 'nt', 'json-ld']

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

class OntologyEnvironment:
    def __init__(self, init_graph = Graph()):
        self.g = init_graph

    def get_serialized_graph(self, req_format='turtle'):
        if req_format not in valid_formats:
            return 'Invalid format', 400
        return self.g.serialize(format=req_format)

    def add_sensor(self,req_name, req_measure ):
        new_sensor_uri = ioto[req_name]
        self.g.add((new_sensor_uri, RDF.type, sosa.Sensor))
        self.g.add((new_sensor_uri, sosa.hasName, Literal(req_name, datatype=XSD.string))) 
        observed_property = measure_to_property.get(req_measure.lower())
        if observed_property:
            self.g.add((new_sensor_uri, sosa.observes, observed_property))
        else:
            return 'Invalid measure', 400
        
        return 'sensor added', 201
        
smart_environment = PythonEnvironment()
ontology_environment = OntologyEnvironment()

@app.route('/sensors')
def list_sensors():
    method = request.args.get('method')
    if method == 'ontology':
        # TODO: make custom SPARQL query to get sensors this is getting all graph by default
        req_format = request.args.get('format')
        return ontology_environment.get_serialized_graph(req_format)
    elif method == 'web':
        return smart_environment.get_sensors()
    else:
        return 'method not recognized', 400


@app.route('/sensors', methods=['POST'])
def add_sensor():
    data = request.get_json()
    name = data.get('name')
    measure = data.get('measure')
    if not name or not measure:
        return 'Invalid sensor data', 422
    method = data.get('method')
    if method == 'ontology':
        return ontology_environment.add_sensor(name, measure)
    elif method == 'web':
        return smart_environment.add_sensor(name, measure)
    else:
        return 'method not recognized', 400

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


# create a method that analyse the observations and get high level info
# create a method that initiate the building instance (set ethic mode and info about data controllers)
# we ca make form to fill in the data


if __name__ == '__main__':
    app.run(port=5000)