from flask import Flask, jsonify, request
import rdflib
from rdflib import Graph, Literal, BNode, Namespace, RDF, XSD, OWL,URIRef


app = Flask(__name__)


# Define namespaces
sosa = Namespace('https://www.w3.org/ns/sosa/')
seas = Namespace('https://w3id.org/seas/')
xsd = Namespace('http://www.w3.org/2001/XMLSchema#')
ioto = Namespace("https://github/ioto/EnhacedOntology4IoT/")

# Define the graph
g = Graph()

sensors = []


@app.route('/sensors')
def get_sensors():
    return jsonify(sensors)

@app.route('/observations')
def get_observations():
    return jsonify(observations)

observations = []

@app.route('/observations', methods=['POST'])
def add_observation():
    # modify this function to check if the sensor is in the list of sensors
    # if not return an error message: explaining that sensor must be register first
    observations.append(request.get_json())
    # add the observation to the graph
    ''' Check this works
    # Define an observation
    observation = URIRef('http://example.org/observation1')
    g.add((observation, RDF.type, sosa.Observation))
    g.add((observation, sosa.madeBySensor, thermostat))
    g.add((observation, sosa.observedProperty, temperature_property))
    g.add((observation, sosa.hasResult, Literal('20', datatype=XSD.float)))  # Assuming the result is 20 Celsius
    '''

    return 'observation received', 201

# create POST method that add a sensor to the list
@app.route('/sensors', methods=['POST'])
def add_sensor():
    sensors.append(request.get_json())
    # check if the sensor is already in the list
    # check if sensor is correctly defined (e.g., has a name, a type, etc.)
    # modify this function to add the sensor to the graph
    ''' Check this works
    thermostat = URIRef('http://example.org/thermostat')
    g.add((thermostat, RDF.type, sosa.Sensor))
    temperature_property = seas.temperature
    g.add((thermostat, sosa.observes, temperature_property))
    '''
    return 'sensor added', 201

@app.route("/")
def welcome_message():
    return "Hello, from smart building!"

# create a GET method that returns the ontology in turtle format
@app.route('/turtle_ontology')
def get_ontology_format_turtle():
    # return the ontology in turtle format
    # upgrade this function to return the ontology in desired format
    return g.serialize(format='turtle').decode('utf-8')

# create a method that analyse the observations and get high level info
# create a method that initiate the building instance (set ethic mode and info about data controllers)
# we ca make form to fill in the data



if __name__ == '__main__':
    app.run(port=5000)