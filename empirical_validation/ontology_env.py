from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, XSD, OWL,URIRef
# Define namespaces
sosa = Namespace('https://www.w3.org/ns/sosa/')
ssn = Namespace("http://www.w3.org/ns/ssn/")
seas = Namespace('https://w3id.org/seas/')
xsd = Namespace('http://www.w3.org/2001/XMLSchema#')
ioto = Namespace("https://github.com/Alex23013/Ioto-Semantic-for-IoT-Environments/blob/main/iot_ontologies/ioto-protege.ttl/")
# module 2
colpri = Namespace("https://github/ioto/EnhacedOntology4IoT/colpri#")
ds4iot = Namespace("https://github/ioto/EnhacedOntology4IoT/ds4iot#")
import base64
from cryptography.fernet import Fernet


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
    def __init__(self, init_graph = Graph(), encryption_key = b'UNxkX76p0EW7Frcx7zux7VFpp5Uxl43FLGD4SxEBppM='):
        self.g = init_graph
        self.g.bind("sosa", sosa)
        self.g.bind("ssn", ssn)
        self.g.bind("ioto", ioto)
        self.g.bind("colpri", colpri)
        self.g.bind("ds4iot", ds4iot)
        # module2
        self.create_data_controller("MuseumAdmin", "VisitorDataProcessing")
        self.insert_identity_data_concept()
        self.museum_admin = ioto.MuseumAdmin
        self.default_encryption_algorithm = ioto.AES256  # Example encryption algorithm
        self.default_security_policy = ioto.GeneralDataProtectionRegulation  # Example policy
        self.cipher = Fernet(encryption_key)

    def get_serialized_graph(self, req_format='turtle'):
        if req_format not in valid_formats:
            return 'Invalid format', 400
        
        serialized_graph = self.g.serialize(format=req_format)

        # Save as a Turtle file
        if req_format == 'turtle': 
            with open("ioto_ontology_instance.ttl", "w", encoding="utf-8") as f:
                f.write(serialized_graph)
        return serialized_graph

    def get_sensors(self):
        query = prepareQuery("""
            SELECT ?device ?sensor ?format ?property ?room WHERE {
                ?device a ioto:IoTDevice .
                ?device ioto:hasSensor ?sensor .
                ?sensor sosa:observes ?property .
                ?sensor ioto:usesDataFormat ?format .
                OPTIONAL { ?device ioto:locatedInRoom ?room }
            }
        """, initNs={"sosa": sosa, "ioto": ioto})

        results = []
        for row in self.g.query(query):
            results.append({
                "device": str(row.device),
                "sensor": str(row.sensor),
                "observes": str(row.property),
                "data_format": str(row.format),
                "room": str(row.room) if row.room else None  # Handle optional room
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
    
    def add_sensor(self, data):
        # Extract parameters
        device_name = data.get('device_name')
        device_type = data.get('device_type')  # LegacyDevice or ModernDevice
        sensor_name = data.get('sensor_name')
        room_name = data.get('room') 
        protocol = data.get('protocol')
        iot_standard = data.get('iot_standard')

        if self.is_created_sensor_name(sensor_name):
            return 'Sensor already exists', 400
        
        measure = data.get('measure')
        data_format = data.get('data_format')

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

        # Create and Link Room (Exhibition)
        if room_name:
            room_uri = ioto[room_name]
            self.g.add((room_uri, RDF.type, ioto.Room))
            self.g.add((room_uri, RDFS.label, Literal(room_name, datatype=XSD.string)))
            self.g.add((device_uri, ioto.locatedInRoom, room_uri))  # Device is in a Room

        # Link IoTDevice to Communication Protocol
        if protocol:
            protocol_uri = ioto[protocol]
            self.g.add((protocol_uri, RDF.type, ioto.CommunicationProtocol))
            self.g.add((protocol_uri, RDFS.label, Literal(protocol, datatype=XSD.string)))
            self.g.add((device_uri, ioto.usesProtocol, protocol_uri))

        # Link IoTDevice to IoT Standard
        if iot_standard:
            standard_uri = ioto[iot_standard]
            self.g.add((standard_uri, RDF.type, ioto.IoTStandard))
            self.g.add((standard_uri, RDFS.label, Literal(iot_standard, datatype=XSD.string)))
            self.g.add((device_uri, ioto.hasStandard, standard_uri))

        return "IoT Device, Sensor, ObservableProperty, Room, Protocol, and Standard linked", 201
    
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
    
    def create_data_controller(self, controller_name, purpose):
        """
        Creates a DataController with a specified purpose.
        """
        controller_uri = ioto[controller_name]
        purpose_uri = ioto[purpose]

        # Create DataController instance
        self.g.add((controller_uri, RDF.type, ioto.DataController))
        self.g.add((controller_uri, RDFS.label, Literal(controller_name, datatype=XSD.string)))

        # Create Purpose and link to DataController
        self.g.add((purpose_uri, RDF.type, ioto.Purpose))
        self.g.add((controller_uri, ioto.definesPurpose, purpose_uri))

        return f"DataController '{controller_name}' created with purpose '{purpose}'."
    
    def insert_identity_data_concept(self):
        """
        Inserts the concept of IdentityData as a subclass of SensitivePersonalData.
        This ensures it follows the restriction of being treated as EncryptedData.
        """
        self.g.add((colpri.IdentityData, RDF.type, OWL.Class))
        self.g.add((colpri.IdentityData, RDFS.subClassOf, colpri.SensitivePersonalData))

        # Define Restriction: IdentityData must be treated as EncryptedData
        restriction_blank_node = BNode()  # Create a blank node for the restriction
        self.g.add((restriction_blank_node, RDF.type, OWL.Restriction))
        self.g.add((restriction_blank_node, OWL.onProperty, ioto.mustBeTreatedAs))
        self.g.add((restriction_blank_node, OWL.someValuesFrom, ds4iot.EncryptedData))

        # Attach restriction to IdentityData
        self.g.add((colpri.IdentityData, RDFS.subClassOf, restriction_blank_node))

        # Define the ontology reference
        self.g.add((colpri.IdentityData, RDFS.isDefinedBy, colpri._URI))

        return "IdentityData concept added to ontology."

    def encrypt_data(self, plaintext: str) -> str:
        """Encrypts the given plaintext using AES-256."""
        encrypted_bytes = self.cipher.encrypt(plaintext.encode())
        return base64.urlsafe_b64encode(encrypted_bytes).decode()  # Store as string

    def add_external_visitor(self, data):
        req_role = data.get('role')
        if req_role == 'visitor':
            self.add_visitor(data)
        else:
            self.add_personal(data) 
        return 'visitor added', 201
    
    def insert_personal_data(self, prop, visitor_id, value, is_sensitive):
        """
        Inserts personal data as either SensitivePersonalData (encrypted) or NonSensitivePersonalData.
        
        :param prop: Property name (e.g., "name", "lastname").
        :param visitor_id: Unique visitor identifier.
        :param value: The actual data to store.
        :param is_sensitive: Boolean indicating if data should be encrypted.
        """
        data_uri = ioto[f"{prop.capitalize()}_{visitor_id}"]
        
        if is_sensitive:
            encrypted_value = self.encrypt_data(value)  # Encrypt the data
            self.g.add((data_uri, RDF.type, colpri.IdentityData))
            self.g.add((data_uri, ioto.encryptedValue, Literal(encrypted_value, datatype=XSD.string)))  # Store encrypted
            self.g.add((data_uri, ioto.mustBeTreatedAs, ds4iot.EncryptedData))  # Link to EncryptedData
        else:
            self.g.add((data_uri, RDF.type, colpri.NonSensitivePersonalData))  # Mark as NonSensitive
        
        # Add label
        self.g.add((data_uri, RDFS.label, Literal(f"{prop.capitalize()} of visitor {visitor_id}", datatype=XSD.string)))
    
    def add_visitor(self, visitor_data):
        visitor_id = visitor_data.get("id")
        consent_given = visitor_data.get("consent")

        # Create Visitor Consent instance
        consent_uri = ioto[f"VisitorConsent_{visitor_id}"]
        consent_type = colpri.GivenConsent if consent_given else colpri.UngivenConsent

        self.g.add((consent_uri, RDF.type, consent_type))
        self.g.add((consent_uri, RDFS.label, Literal(f"Consent for visitor {visitor_id}", datatype=XSD.string)))

        # Link MuseumAdmin to the Consent
        self.g.add((self.museum_admin, ioto.makesConsent, consent_uri))
        
        # Insert personal data (Sensitive or Non-Sensitive)
        personal_data_properties = {
            "gender": False,   # Non-sensitive (NonSensitivePersonalData)
            "name": True,     # Always sensitive (IdentityData)
            "lastname": True  # Always sensitive (IdentityData)
        }

        for prop, is_sensitive in personal_data_properties.items():
            value = visitor_data.get(prop)
            if value:
                self.insert_personal_data(prop, visitor_id, value, is_sensitive)
        
        # Define encryption method and security policy
        encryption_method_uri = ioto[f"EncryptionMethod_{visitor_id}"]
        self.g.add((encryption_method_uri, RDF.type, ioto.EncryptionMethod))
        self.g.add((encryption_method_uri, ioto.usesEncryptionAlgorithm, self.default_encryption_algorithm))

        # Link encrypted data to encryption method and security policy
        self.g.add((ds4iot.EncryptedData, ioto.hasEncryptionMethod, encryption_method_uri))
        self.g.add((ds4iot.EncryptedData, ioto.followsSecurityPolicy, self.default_security_policy))

        return f"Visitor Consent ({'Given' if consent_given else 'Ungiven'}) and IdentityData added for visitor {visitor_id}.", 201

    def add_personal(self, personal_data):
        personal_id = personal_data.get("id")

        # Create Personal Consent instance (always GivenConsent)
        consent_uri = ioto[f"PersonalConsent_{personal_id}"]
        self.g.add((consent_uri, RDF.type, colpri.GivenConsent))
        self.g.add((consent_uri, RDFS.label, Literal(f"Consent for personal {personal_id}", datatype=XSD.string)))

        # Link MuseumAdmin to the Consent
        self.g.add((self.museum_admin, ioto.makesConsent, consent_uri))

        return "Personal Consent (Given) added.", 201