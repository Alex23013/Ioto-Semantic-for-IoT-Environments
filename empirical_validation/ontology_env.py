from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, XSD, OWL,URIRef
# Define namespaces
sosa = Namespace('https://www.w3.org/ns/sosa/')
ssn = Namespace("http://www.w3.org/ns/ssn/")
seas = Namespace('https://w3id.org/seas/')
xsd = Namespace('http://www.w3.org/2001/XMLSchema#')
ioto = Namespace("https://github.com/Alex23013/Ioto-Semantic-for-IoT-Environments/blob/main/iot_ontologies/ioto-protege.ttl/")

from rdflib.plugins.sparql import prepareQuery

# Define namespaces for SPARQL queries
#ioto = Namespace("http://example.com/ioto#")

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
        self.g.bind("sosa", sosa)
        self.g.bind("ssn", ssn)
        self.g.bind("ioto", ioto)

    def get_serialized_graph(self, req_format='turtle'):
        if req_format not in valid_formats:
            return 'Invalid format', 400
        
        serialized_graph = self.g.serialize(format=req_format)

        # Save as a Turtle file
        if req_format == 'turtle':  # Only save when the format is Turtle
            with open("ioto_ontology_instance.ttl", "w", encoding="utf-8") as f:
                f.write(serialized_graph)
        return serialized_graph

    def get_sensors(self):
        query = prepareQuery("""
            SELECT ?device ?sensor ?format ?property WHERE {
                ?device a ioto:IoTDevice .
                ?device ioto:hasSensor ?sensor .
                ?sensor sosa:observes ?property .
                ?sensor ioto:usesDataFormat ?format .
            }
        """, initNs={"sosa": sosa, "ioto": ioto})

        results = []
        for row in self.g.query(query):
            results.append({
                "device": str(row.device),
                "sensor": str(row.sensor),
                "observes": str(row.property),
                "data_format": str(row.format)
            })
        return results

    def is_created_sensor_name(self, sensor_name):
        query = prepareQuery("""
            ASK {
                ?sensor a sosa:Sensor .
                ?sensor rdfs:label ?name .
                FILTER(?name = ?sensor_name)
            }
        """, initNs={"sosa": sosa, "rdfs": RDFS})

        result = self.g.query(query, initBindings={"sensor_name": Literal(sensor_name, datatype=XSD.string)})
        return bool(result.askAnswer)
    '''
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
        
        return 'sensor added', 201'
    '''


    
    def add_sensor(self, data):
        # Extract parameters
        device_name = data.get('device_name')
        device_type = data.get('device_type')  # LegacyDevice or ModernDevice
        sensor_name = data.get('sensor_name')
        if self.is_created_sensor_name(sensor_name):
            return 'Sensor already exists', 400
        
        measure = data.get('measure')  # e.g., "Temperature"
        data_format = data.get('data_format')  # e.g., "JSON"

        # Create IoTDevice
        device_uri = ioto[device_name]
        self.g.add((device_uri, RDF.type, ioto.IoTDevice))  
        
        # Assign subclass if specified
        if device_type == "LegacyDevice":
            self.g.add((device_uri, RDF.type, ioto.LegacyDevice))
        elif device_type == "ModernDevice":
            self.g.add((device_uri, RDF.type, ioto.ModernDevice))

        self.g.add((device_uri, RDFS.label, Literal(device_name, datatype=XSD.string)))

        # Create Sensor
        sensor_uri = ioto[sensor_name]
        self.g.add((sensor_uri, RDF.type, sosa.Sensor))
        self.g.add((sensor_uri, RDFS.label, Literal(sensor_name, datatype=XSD.string)))

        # Create ObservableProperty
        property_uri = ioto[measure]
        self.g.add((property_uri, RDF.type, sosa.ObservableProperty))
        self.g.add((property_uri, RDFS.label, Literal(measure, datatype=XSD.string)))

        # Link Sensor to ObservableProperty
        self.g.add((sensor_uri, sosa.observes, property_uri))

        # Link Sensor to DataFormat
        format_uri = ioto[data_format]
        self.g.add((format_uri, RDF.type, ioto.DataFormat))
        self.g.add((sensor_uri, ioto.usesDataFormat, format_uri))

        # Link IoTDevice to Sensor
        self.g.add((device_uri, ioto.hasSensor, sensor_uri))

        return "IoT Device, Sensor, and ObservableProperty added", 201
    
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

    def add_visitor(self, data):
        req_name = data.get('name')
        req_role = data.get('role')
        new_visitor_uri = ioto[req_name]
        self.g.add((new_visitor_uri, RDF.type, ioto.Visitor)) #TODO: ver como modelar a las personas
        self.g.add((new_visitor_uri, ioto.hasRole, Literal(req_role, datatype=XSD.string))) 
        return 'visitor added', 201
# create a method that analyse the observations and get high level info