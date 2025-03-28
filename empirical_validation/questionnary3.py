from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, XSD, OWL,URIRef
# Define namespaces
sosa = Namespace('https://www.w3.org/ns/sosa/')
ssn = Namespace("http://www.w3.org/ns/ssn/")
seas = Namespace('https://w3id.org/seas/')
xsd = Namespace('http://www.w3.org/2001/XMLSchema#')
ioto = Namespace("https://github.com/Alex23013/Ioto-Semantic-for-IoT-Environments/blob/main/iot_ontologies/ioto-protege.ttl/")
colpri = Namespace("https://github/ioto/EnhacedOntology4IoT/colpri#")
ds4iot = Namespace("https://github/ioto/EnhacedOntology4IoT/ds4iot#")

from rdflib.plugins.sparql import prepareQuery
import time

# TODO: this questions are mocked still need to be implemented

class QuestionnaryModule3:
    def __init__(self, result_mode, file_path="ioto_ontology_instance.ttl"):
        self.g = Graph()
        self.g.parse(file_path, format="turtle")
        self.g.bind("sosa", sosa)
        self.g.bind("colpri", colpri)
        self.g.bind("ioto", ioto)
        self.result_mode = result_mode
        self.module_name = "Questionnary Module 3: Security"

    def mod3_qa(self):
        start_time = time.time()
        query = prepareQuery("""
            SELECT DISTINCT ?dataItem ?encryptionMethod ?algorithm ?securityPolicy ?cryptoManager
            WHERE {
                ?dataItem ioto:mustBeTreatedAs ds4iot:EncryptedData .
                OPTIONAL { ?dataItem ioto:hasEncryptionMethod ?encryptionMethod . }
                OPTIONAL { ?encryptionMethod ioto:usesEncryptionAlgorithm ?algorithm . }
                OPTIONAL { ?dataItem ioto:followsSecurityPolicy ?securityPolicy . }
                OPTIONAL { ?dataItem ds4iot:hasCryptoManager ?cryptoManager . }
            }
        """, initNs={"ds4iot": ds4iot, "ioto": ioto, "colpri": colpri})

        results = []
        for row in self.g.query(query):
            results.append({
                "dataItem": row.dataItem,
                "encryptionMethod": row.encryptionMethod,
                "algorithm": row.algorithm,
                "securityPolicy": row.securityPolicy,
                "cryptoManager": row.cryptoManager
            })
        end_time = time.time()
        execution_time = end_time - start_time
        if self.result_mode=='time':
            return f"{execution_time:.4f} seconds"
        return results
    
    def mod3_qb(self):
        start_time = time.time()
        query = prepareQuery("""
            SELECT DISTINCT ?entity ?accessControl ?securityPolicy
            WHERE {
                {
                    ?entity a ioto:IoTDevice .
                }
                UNION
                {
                    ?entity ioto:followsSecurityPolicy ?securityPolicy .
                }
                UNION
                {
                    ?entity ioto:triggersAccessControl ?accessControl .
                }
                OPTIONAL { ?entity ioto:triggersAccessControl ?accessControl . }
                OPTIONAL { ?entity ioto:followsSecurityPolicy ?securityPolicy . }
            }
        """, initNs={"ioto": ioto})
        
        results = []
        for row in self.g.query(query):
            results.append({
                "entity": row.entity,
                "accessControl": row.accessControl,
                "securityPolicy": row.securityPolicy
            })

        end_time = time.time()
        execution_time = end_time - start_time
        if self.result_mode == 'time':
            return f"{execution_time:.4f} seconds"
        return results

    
    def mod3_qc(self):
        start_time = time.time()
        query = prepareQuery("""
            SELECT ?anomaly ?abnormalBehavior ?device ?monitor
            WHERE {
            ?anomaly a ioto:Anomaly ;
                    ioto:representsAbnormalBehavior ?abnormalBehavior ;
                    ioto:detectedBy ?monitor .

            ?device ioto:hasBehavior ?abnormalBehavior .
            }            
        """, initNs={"ioto": ioto})
        results = []
        for row in self.g.query(query):
            results.append({      
                "anomaly": str(row.anomaly),
                "abnormal_behavior": str(row.abnormalBehavior),
                "device": str(row.device),
                "monitor": str(row.monitor)        
            })
        end_time = time.time()
        execution_time = end_time - start_time
        if self.result_mode=='time':
            return f"{execution_time:.4f} seconds"
        return results
    
    def mod3_qd(self):
        start_time = time.time()
        query = prepareQuery("""
           SELECT ?anomaly ?threatResponse ?incidentManager
            WHERE {
                ?anomaly a ioto:Anomaly ;
                        ioto:requiresResponse ?threatResponse .
                        
                ?threatResponse a ioto:ThreatResponse ;
                                rdfs:label ?responseDescription .

                OPTIONAL {
                    ?incidentManager a ioto:IncidentResponseManager ;
                                    ioto:handlesIncident ?threatResponse .
                }
            }       
        """, initNs={"ioto": ioto, "rdfs": RDFS})
        results = []
        for row in self.g.query(query):
            results.append({     
                "anomaly": str(row.anomaly),
                "threat_response": str(row.threatResponse),
                "incident_manager": str(row.incidentManager)
            })
        end_time = time.time()
        execution_time = end_time - start_time
        if self.result_mode=='time':
            return f"{execution_time:.4f} seconds"
        return results