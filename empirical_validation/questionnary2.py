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

class QuestionnaryModule2:
    def __init__(self, result_mode, file_path="ioto_ontology_instance.ttl"):
        self.g = Graph()
        self.g.parse(file_path, format="turtle")
        self.g.bind("sosa", sosa)
        self.g.bind("colpri", colpri)
        self.g.bind("ioto", ioto)
        self.result_mode = result_mode
        self.module_name = "Questionnary Module 2: Privacy Policy"

    def mod2_qa(self):
        start_time = time.time()
        query = prepareQuery("""
            SELECT DISTINCT ?user ?consentType ?consentLabel
            WHERE {
                ?user a ioto:DataController ;  
                    ioto:makesConsent ?consent .      

                ?consent a ?consentType ;
                        rdfs:label ?consentLabel .  
                        
                # Ensure the consent type is specifically GivenConsent or UngivenConsent
                FILTER (?consentType IN (colpri:GivenConsent, colpri:UngivenConsent))
            }
        """, initNs={"ioto": ioto, "colpri": colpri})

        results = []
        for row in self.g.query(query):
            results.append({
                "user": str(row.user),
                "consent_type": str(row.consentType),
                "consent_label": str(row.consentLabel)
            })
        end_time = time.time()
        execution_time = end_time - start_time
        if self.result_mode=='time':
            return f"{execution_time:.4f} seconds"
        return results
    
    def mod2_qb(self):
        start_time = time.time()
        query = prepareQuery("""
            SELECT DISTINCT ?dataInstance ?dataType (COALESCE(?encryptionStatus, "Not Encrypted") AS ?finalStatus)
            WHERE {
                ?dataInstance a ?subType .
                ?subType rdfs:subClassOf* ?dataType .

                # Check if data is encrypted
                OPTIONAL {
                    ?dataInstance ioto:mustBeTreatedAs ds4iot:EncryptedData .
                    BIND("Encrypted" AS ?encryptionStatus)
                }

                FILTER (?dataType IN (colpri:SensitivePersonalData, colpri:NonSensitivePersonalData))
            }
        """, initNs={"colpri": colpri, "ioto": ioto, "ds4iot": ds4iot, "rdfs": RDFS})
        
        results = []
        for row in self.g.query(query):
            results.append({
                "data_instance": str(row.dataInstance),
                "data_type": str(row.dataType),
                "encryption_status": str(row.finalStatus)
            })

        end_time = time.time()
        execution_time = end_time - start_time
        if self.result_mode == 'time':
            return f"{execution_time:.4f} seconds"
        return results

    
    def mod2_qc(self):
        start_time = time.time()
        query = prepareQuery("""
            SELECT ?dataDomain ?accessControl
            WHERE {
            ?dataDomain ds4iot:hasAccessControl
            ?accessControl .
            }            
        """, initNs={"ds4iot": ds4iot})
        results = []
        for row in self.g.query(query):
            results.append({    
                "data_domain": str(row.dataDomain),
                "access_control": str(row.accessControl)         
            })
        end_time = time.time()
        execution_time = end_time - start_time
        if self.result_mode=='time':
            return f"{execution_time:.4f} seconds"
        return results
    
    def mod2_qd(self):
        start_time = time.time()
        query = prepareQuery("""
            SELECT DISTINCT ?device ?dataDomain
            ?accessControlModel
            WHERE {
            ?device a ioto:IoTDevice .
            ?device ioto:generatesData ?dataDomain .
            ?dataDomain ds4iot:hasAccessControl
            ?accessControlModel .
            }
        """, initNs={"ioto": ioto, "ds4iot": ds4iot})
        results = []
        for row in self.g.query(query):
            results.append({      
                "device": str(row.device),
                "data_domain": str(row.dataDomain),
                "access_control_model": str(row.accessControlModel)        
            })
        end_time = time.time()
        execution_time = end_time - start_time
        if self.result_mode=='time':
            return f"{execution_time:.4f} seconds"
        return results