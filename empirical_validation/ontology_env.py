from rdflib import Graph, Literal, BNode, Namespace, RDF, XSD, OWL,URIRef
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


class OntologyEnvironment:
    def __init__(self, init_graph = Graph()):
        self.g = init_graph

    def get_serialized_graph(self, req_format='turtle'):
        if req_format not in valid_formats:
            return 'Invalid format', 400
        return self.g.serialize(format=req_format)

    def add_sensor(self, data):
        req_name = data.get('name')
        req_measure = data.get('measure')
        new_sensor_uri = ioto[req_name]
        self.g.add((new_sensor_uri, RDF.type, sosa.Sensor))
        self.g.add((new_sensor_uri, sosa.hasName, Literal(req_name, datatype=XSD.string))) 
        observed_property = measure_to_property.get(req_measure.lower())
        if observed_property:
            self.g.add((new_sensor_uri, sosa.observes, observed_property))
        else:
            return 'Invalid measure', 400
        
        return 'sensor added', 201
    
    def add_observation(self, data):
        #TODO: SPARQL for get sensor measure and name based in sensor_name
        found_sensor = None
        # Get the observed property dynamically based on the sensor's measure
        observed_property = measure_to_property.get(found_sensor.measure.lower())
        if not observed_property:
            return 'Invalid measure', 400
        observations = [] #TODO: SPARQL for  get observations from sensor
        num_obs = len(observations)
        observation = ioto[found_sensor.name + '_observation_'+str(num_obs)]
        self.g.add((observation, RDF.type, sosa.Observation))
        self.g.add((observation, sosa.madeBySensor, URIRef(ioto[found_sensor.name])))
        self.g.add((observation, sosa.observedProperty, observed_property))
        self.g.add((observation, sosa.hasResult, Literal(data.value, datatype=XSD.float)))
        # TODO: add timestamp
        return 'observation received', 201

# create a method that analyse the observations and get high level info