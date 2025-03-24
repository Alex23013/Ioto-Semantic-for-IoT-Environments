from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, XSD, OWL,URIRef
# Define namespaces
sosa = Namespace('https://www.w3.org/ns/sosa/')
seas = Namespace('https://w3id.org/seas/')
xsd = Namespace('http://www.w3.org/2001/XMLSchema#')
ioto = Namespace("https://github.com/Alex23013/Ioto-Semantic-for-IoT-Environments/blob/main/iot_ontologies/ioto-protege.ttl/")
# module2
colpri = Namespace("https://github/ioto/EnhacedOntology4IoT/colpri#")
ds4iot = Namespace("https://github/ioto/EnhacedOntology4IoT/ds4iot#")
import base64
from cryptography.fernet import Fernet
from flask import jsonify
from datetime import datetime


from rdflib.plugins.sparql import prepareQuery

DEBUG_MODE = True
# Constants
valid_formats = ['turtle', 'xml', 'n3', 'nt', 'json-ld']

class OntologyEnvironment:
    def __init__(self, continue_instance,  encryption_key = b'UNxkX76p0EW7Frcx7zux7VFpp5Uxl43FLGD4SxEBppM='):
        self.g = Graph()
        if continue_instance:
            file_path="ioto_ontology_instance.ttl"
            self.g.parse(file_path, format="turtle")
        self.g.bind("sosa", sosa)
        self.g.bind("ioto", ioto)
        self.g.bind("seas", seas)
        self.g.bind("colpri", colpri)
        self.g.bind("ds4iot", ds4iot)
        # module2
        self.data_contoller_uri = self.create_data_controller("MuseumAdmin", "VisitorDataProcessing")
        self.insert_identity_data_concept()
        self.museum_admin = ioto.MuseumAdmin
        # module3
        self.default_encryption_algorithm = ioto.AES256  # Example encryption algorithm
        self.crypto_manager_uri, self.encryption_method_uri = self.create_crypto_manager_and_encryption_algorithm("Museum_CryptoManager")
        self.default_security_policy = ioto.GeneralDataProtectionRegulation  # Example policy
        self.encrypted_security_policy = ioto.EncryptedDataProtectionRegulation  # Encrypted policy
        self.moderate_security_policy = ioto.ModerateDataProtectionRegulation  # Moderate policy
        self.cipher = Fernet(encryption_key)
        self.response_manager = self.create_incident_response_manager("MuseumIncidentResponseManager")
        # module4 
        self.thermal_energy = seas.ThermalEnergy
        self.chemical_energy = seas.ChemicalEnergy 
        self.light_energy =  ioto.LightEnergy
        self.acoustic_energy = ioto.AcousticEnergy
        self.g.add((self.thermal_energy, RDF.type, seas.EnergyForm))
        self.g.add((self.chemical_energy, RDF.type, seas.EnergyForm))
        self.g.add((self.light_energy, RDF.type, seas.EnergyForm))
        self.g.add((self.acoustic_energy, RDF.type, seas.EnergyForm))
        self.energy_form_map = {
            "temperature": {
                "energy_form": self.thermal_energy,
                "control_action_desc": "Adjusts heating or cooling to regulate temperature.",
                "sustainability_metric": "EnergyEfficiency"
            },
            "air_quality": {
                "energy_form": self.chemical_energy,
                "control_action_desc": "Activates air purifiers or ventilation to improve air quality.",
                "sustainability_metric": "AirQualityIndex"
            },
            "illumination": {
                "energy_form": self.light_energy,
                "control_action_desc": "Adjusts lighting intensity for optimal illumination.",
                "sustainability_metric": "LightingEfficiency"
            },
            "noise": {
                "energy_form": self.acoustic_energy,
                "control_action_desc": "Activates noise-canceling systems or sound dampening.",
                "sustainability_metric": "AcousticComfort"
            },
            "smoke": {
                "energy_form": self.chemical_energy,
                "control_action_desc": "Triggers alarms or activates ventilation to handle smoke.",
                "sustainability_metric": "SafetyRiskIndex"
            }
        }


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
        threshold = data.get('threshold')

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

         # Add threshold if provided
        if threshold is not None:
            self.g.add((device_uri, ioto.hasThreshold, Literal(float(threshold), datatype=XSD.float)))
            
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
        # Link ObservableProperty to EnergyForm if available
        energy_data = self.energy_form_map.get(measure)
        if energy_data:
            energy_form = energy_data["energy_form"]
            control_desc = energy_data["control_action_desc"]
            sustainability_metric_name = energy_data["sustainability_metric"]

            # Link ObservableProperty to EnergyForm
            self.g.add((property_uri, ioto.associatedEnergyForm, energy_form))
            
            # Create ControlAction linked to this EnergyForm with description
            control_action_uri = ioto[f"ControlAction_{sensor_name}"]
            self.g.add((control_action_uri, RDF.type, ioto.ControlAction))
            self.g.add((control_action_uri, RDFS.label, Literal(control_desc, datatype=XSD.string)))
            self.g.add((control_action_uri, ioto.adjusts, energy_form))

            # Create SustainabilityMetric instance
            sustainability_metric_uri = ioto[f"{sustainability_metric_name}_{sensor_name}"]
            self.g.add((sustainability_metric_uri, RDF.type, ioto.SustainabilityMetric))
            self.g.add((sustainability_metric_uri, RDFS.label, Literal(sustainability_metric_name, datatype=XSD.string)))

            # Link the Sensor to the SustainabilityMetric using ioto:assessesMetric
            self.g.add((sensor_uri, ioto.assessesMetric, sustainability_metric_uri))


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

        # Create DataDomain generated by the device
        data_domain_uri = ioto[f"{device_name}_DataDomain"]
        self.g.add((data_domain_uri, RDF.type, ioto.DataDomain))
        self.g.add((data_domain_uri, RDFS.label, Literal(f"{device_name} Data Domain", datatype=XSD.string)))
        self.g.add((device_uri, ioto.generatesData, data_domain_uri))

        # Create AccessControl (default RBAC example)
        access_control_uri = ds4iot[f"{device_name}_RBAC"]
        self.g.add((access_control_uri, RDF.type, ds4iot.RBAC))
        self.g.add((access_control_uri, RDFS.label, Literal(f"{device_name} RBAC", datatype=XSD.string)))

        # Link DataDomain to AccessControl
        self.g.add((data_domain_uri, ds4iot.hasAccessControl, access_control_uri))

        # Link IoTDevice to the AccessControl it triggers
        self.g.add((device_uri, ioto.triggersAccessControl, access_control_uri))
        self.g.add((device_uri, ioto.followsSecurityPolicy, self.moderate_security_policy))

        # Create and link SecurityMonitor
        monitor_uri = ioto[f"SecurityMonitor_for_{device_name}"]
        self.g.add((monitor_uri, RDF.type, ioto.SecurityMonitor))
        self.g.add((monitor_uri, RDFS.label, Literal(f"SecurityMonitor for {device_name}", datatype=XSD.string)))
        self.g.add((monitor_uri, ioto.monitors, device_uri))

        return "IoT Device, Sensor, ObservableProperty, Room, Protocol, and Standard linked", 201
    
    def add_observation(self, data):
        sensor_name = data.get('sensor')
        sensor_value = data.get('value')
        evaluation_value = data.get('evaluation')
        
        # Get sensor URI
        sensor_uri = ioto[sensor_name]
        if not sensor_uri:
            return 'Sensor not found', 404
        
        # SPARQL query to get the observed property of the sensor
        query = f"""
        SELECT ?observed_property WHERE {{
            ioto:{sensor_name} sosa:observes ?observed_property .
        }}
        """
        results = self.g.query(query, initNs={'sosa': sosa, 'ioto': ioto})
        if DEBUG_MODE:
            print("results of SPARQL query")
        for row in self.g.query(query):
            results.append({
                "observed_property": row.observed_property
            })
        # Get the observed property
        observed_property = None
        for row in results:
            observed_property = row.observed_property

        if not observed_property:
            return 'Observable property not found', 404

        # Count existing observations of this sensor
        obs_query = f"""
        SELECT (COUNT(?obs) as ?count) WHERE {{
            ?obs sosa:madeBySensor ioto:{sensor_name} .
        }}
        """
        obs_result = self.g.query(obs_query, initNs={'sosa': sosa, 'ioto': ioto})
        num_obs = 0
        for row in obs_result:
            num_obs = int(row[0].toPython())
        if DEBUG_MODE:
            print(f"Number of observations found for {sensor_name}: {num_obs}")
        # Create Observation instance
        observation_uri = ioto[f"{sensor_name}_observation_{num_obs + 1}"]
        self.g.add((observation_uri, RDF.type, sosa.Observation))
        self.g.add((observation_uri, sosa.madeBySensor, sensor_uri))
        self.g.add((observation_uri, sosa.observedProperty, observed_property))
        
        # Add simple result (your value) and timestamp
        self.g.add((observation_uri, sosa.hasSimpleResult, Literal(sensor_value, datatype=XSD.float)))
        now = datetime.now().isoformat()
        self.g.add((observation_uri, sosa.resultTime, Literal(now, datatype=XSD.dateTime)))
        self.update_iot_device_behavior(sensor_name, sensor_value, num_obs)
        observed_property_name = observed_property.split("/")[-1]
        self.add_evaluation(observed_property_name ,observed_property, evaluation_value, f"{sensor_name}_observation_{num_obs + 1}", sensor_name)
        return f'Observation added: {observation_uri}', 201
    
    def add_evaluation(self,observed_property_name, observed_property_uri, evaluation_value, observation_name, sensor_name):
        """
        Adds a SEAS Evaluation linked to an ObservableProperty, with an evaluated value.
        Expects: observed_property_uri, evaluation_value, observation_name
        """
        # Create URIs
        evaluation_uri = ioto[f"Evaluation_{observed_property_name}"]
        evaluation_label = f"Evaluation for {observation_name}"
        print("ADD Evaluation method")
        print("evaluation_uri",evaluation_uri)
        print("evaluation_label",evaluation_label)

        # Add Evaluation as a seas:Evaluation instance
        self.g.add((evaluation_uri, RDF.type, seas.Evaluation))
        self.g.add((evaluation_uri, RDFS.label, Literal(evaluation_label, datatype=XSD.string)))

        # Link Evaluation to the Property
        #TODO:check why i am having ns1: in the result instead of seas:
        self.g.add((observed_property_uri, seas.evaluation, evaluation_uri))
        self.g.add((evaluation_uri, seas.evaluationOf, observed_property_uri))

        # Add the evaluated value (can be a qualitative or quantitative literal)
        self.g.add((evaluation_uri, seas.evaluatedValue, Literal(evaluation_value, datatype=XSD.string)))
        
        # SPARQL to fetch the sustainability metric related to the sensor using ioto:assessesMetric
        query = prepareQuery("""
            SELECT ?sustainabilityMetric
            WHERE {
                ?sensor a sosa:Sensor ;
                        rdfs:label ?label ;
                        ioto:assessesMetric ?sustainabilityMetric .
                FILTER(str(?label) = "illuminationSensor01")
            }            
        """, initNs={"ioto": ioto, "sosa": sosa})
        results = []
        for row in self.g.query(query):
            results.append({      
                "sustainabilityMetric": row.sustainabilityMetric     
            })
        print("results metrics")
        print(results)
        if results:
            sustainability_metric_uri = results[0].get('sustainabilityMetric')
            self.g.add((evaluation_uri, ioto.relatesToMetric, sustainability_metric_uri))
            print(f"Linked to sustainability metric: {sustainability_metric_uri}")
        else:
            print("Sustainability metric not found")

        return f"Evaluation for {observed_property_name} added.", 200
    
    def update_iot_device_behavior(self, sensor_name, sensor_value, num_obs):
        # Fetch the IoT Device linked to the sensor
        device_query = f"""
        SELECT ?device WHERE {{
            ?device ioto:hasSensor ioto:{sensor_name} .
        }}
        """
        result = self.g.query(device_query, initNs={'ioto': ioto})
        device_uri = None
        for row in result:
            device_uri = row.device
        if not device_uri:
            return 'Device not found', 404

        # Update device current value
        self.g.set((device_uri, ioto.hasCurrentValue, Literal(sensor_value, datatype=XSD.float)))
        # Check threshold
        threshold_query = f"""
        SELECT ?threshold WHERE {{
            <{device_uri}> ioto:hasThreshold ?threshold .
        }}
        """
        threshold_result = self.g.query(threshold_query, initNs={'ioto': ioto})
        threshold = None
        for row in threshold_result:
            threshold = row.threshold.toPython() # Convert to Python type
        sensor_value = float(sensor_value)
        if threshold is not None and sensor_value > threshold:
            # Abnormal Behavior
            self.g.set((device_uri, ioto.hasBehavior, ioto.AbnormalBehavior))

            # Create Anomaly
            anomaly_uri = ioto[f"Anomaly_{sensor_name}_{num_obs}"]
            self.g.add((anomaly_uri, RDF.type, ioto.Anomaly))

            # Link to SecurityMonitor
            monitor_query = """
                SELECT ?monitor WHERE {
                    ?monitor a ioto:SecurityMonitor ;
                            ioto:monitors ?device .
                }
            """
            monitor_result = self.g.query(monitor_query, initNs={'ioto': ioto}, initBindings={'device': device_uri})
            monitor_uri = None
            for row in monitor_result:
                monitor_uri = row.monitor
                if DEBUG_MODE:
                    print(f"SecurityMonitor found: {monitor_uri}")
            if not monitor_uri:
                # Create SecurityMonitor if not found
                if DEBUG_MODE:
                    print(f"No SecurityMonitor found for {device_uri}, creating one...")
                monitor_uri = ioto[f"SecurityMonitor_for_{sensor_name}"]
                self.g.add((monitor_uri, RDF.type, ioto.SecurityMonitor))
                self.g.add((monitor_uri, ioto.monitors, device_uri))

            # Link the monitor to the detected anomaly
            self.g.add((monitor_uri, ioto.detectsAnomaly, anomaly_uri))
            # Add the inverse relationship detectedBy
            self.g.add((anomaly_uri, ioto.detectedBy, monitor_uri))

            # Create SecurityEvent
            event_uri = ioto[f"SecurityEvent_{sensor_name}_{num_obs}"]
            self.g.add((event_uri, RDF.type, ioto.SecurityEvent))
            # Link Anomaly to AbnormalBehavior
            self.g.add((anomaly_uri, ioto.representsAbnormalBehavior, ioto.AbnormalBehavior))


            # Create ThreatResponse and link it with requiresResponse
            response_uri = ioto[f"ThreatResponse_{sensor_name}_{num_obs}"]
            self.g.add((response_uri, RDF.type, ioto.ThreatResponse))
            self.g.add((response_uri, RDFS.label, Literal(f"Threat response for anomaly detected by {sensor_name}", datatype=XSD.string)))
            self.g.add((anomaly_uri, ioto.requiresResponse, response_uri))

            if hasattr(self, 'response_manager') and self.response_manager:
                self.g.add((self.response_manager, ioto.handlesIncident, response_uri))
                if DEBUG_MODE:
                    print(f"IncidentResponseManager '{self.response_manager}' handles {response_uri}")

            # Link Anomaly to SecurityEvent
            self.g.add((anomaly_uri, ioto.triggersAlert, event_uri))
        else:
            # Normal Behavior
            self.g.set((device_uri, ioto.hasBehavior, ioto.NormalBehavior))

        return 'Device behavior updated', 201

    
    # module2
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
        
        #Add concepts for consent
        self.g.add((colpri.GivenConsent, RDFS.subClassOf, ioto.Consent))
        self.g.add((colpri.UngivenConsent, RDFS.subClassOf, ioto.Consent))
        print(f"DataController '{controller_name}' created with purpose '{purpose}'.")
        return controller_uri
    
    def create_crypto_manager_and_encryption_algorithm(self, manager_name):
        crypto_manager_uri = ds4iot[manager_name]
        self.g.add((crypto_manager_uri, RDF.type, ds4iot.CryptoManager))
        self.g.add((crypto_manager_uri, RDFS.label, Literal(manager_name, datatype=XSD.string)))
        print(f"CryptoManager '{manager_name}' added to IoT instance.")
        encryption_method_uri = ioto[f"EncryptionMethod_for_IoT_instance"]
        self.g.add((encryption_method_uri, RDF.type, ioto.EncryptionMethod))
        self.g.add((encryption_method_uri, ioto.usesEncryptionAlgorithm, self.default_encryption_algorithm))
        print(f"EncryptionMethod '{self.default_encryption_algorithm}' added to IoT instance.")
        return crypto_manager_uri, encryption_method_uri
    
    def create_incident_response_manager(self, manager_name):
        manager_uri = ioto[manager_name]
        self.g.add((manager_uri, RDF.type, ioto.IncidentResponseManager))
        self.g.add((manager_uri, RDFS.label, Literal(manager_name, datatype=XSD.string)))
        print(f"IncidentResponseManager '{manager_name}' created.")
        return manager_uri
    
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

        return "IdentityData concept with CryptoManager added to ontology."

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
    
    def insert_personal_data(self, prop, visitor_id, value, is_sensitive, encryption_method_uri = None):
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
            self.g.add((data_uri, ioto.mustBeTreatedAs, ds4iot.EncryptedData))
            
            self.g.add((data_uri, ds4iot.hasCryptoManager, self.crypto_manager_uri))
            # Link encrypted data to encryption method and security policy
            self.g.add((data_uri, ioto.hasEncryptionMethod, self.encryption_method_uri))
            self.g.add((data_uri, ioto.followsSecurityPolicy, self.encrypted_security_policy))
        else:
            self.g.add((data_uri, RDF.type, colpri.NonSensitivePersonalData))
            self.g.add((data_uri, ioto.followsSecurityPolicy, self.default_security_policy))
        return data_uri

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
                self.insert_personal_data(prop, visitor_id, value, is_sensitive, self.encryption_method_uri)

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
    
    def count_consents_by_data_controller(self):
        """
        Counts the number of ioto:Consent instances made by ioto:DataController.
        """
        query = prepareQuery("""
            SELECT (COUNT(?consent) AS ?consentCount)
            WHERE {
                ?controller a ioto:DataController ;
                            ioto:makesConsent ?consent .
                ?consent a ?consentType .
                FILTER (?consentType IN (colpri:GivenConsent, colpri:UngivenConsent))
            }
        """, initNs={"ioto": ioto, "colpri": colpri})

        result = self.g.query(query)

        # Extract the count from the result
        for row in result:
            return jsonify({"consent_count": int(row.consentCount)}), 200  # Return JSON

        return jsonify({"consent_count": 0}), 200  # Default return value