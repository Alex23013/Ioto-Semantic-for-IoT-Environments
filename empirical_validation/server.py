from flask import Flask, jsonify, request
import rdflib
from rdflib import Graph, Literal, BNode, Namespace, RDF, XSD, OWL,URIRef
from ontology_env import OntologyEnvironment
from python_env import PythonEnvironment

app = Flask(__name__)

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