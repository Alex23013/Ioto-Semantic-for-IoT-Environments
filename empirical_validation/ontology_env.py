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