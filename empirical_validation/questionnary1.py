from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, XSD, OWL,URIRef
# Define namespaces
sosa = Namespace('https://www.w3.org/ns/sosa/')
ssn = Namespace("http://www.w3.org/ns/ssn/")
seas = Namespace('https://w3id.org/seas/')
xsd = Namespace('http://www.w3.org/2001/XMLSchema#')
ioto = Namespace("https://github.com/Alex23013/Ioto-Semantic-for-IoT-Environments/blob/main/iot_ontologies/ioto-protege.ttl/")

from rdflib.plugins.sparql import prepareQuery
import time


class QuestionnaryModule1:
    def __init__(self, result_mode, file_path="ioto_ontology_instance.ttl"):
        self.g = Graph()
        self.g.parse(file_path, format="turtle")
        self.g.bind("sosa", sosa)
        self.g.bind("ssn", ssn)
        self.g.bind("ioto", ioto)
        self.result_mode = result_mode
        self.module_name = "Questionnary Module 1: Interoptability"

    def cat1_qa(self):
        start_time = time.time()
        query = prepareQuery("""
            SELECT DISTINCT ?device ?sensor ?dataFormat
            WHERE {
            ?device a ioto:IoTDevice .
            ?device ioto:hasSensor ?sensor .
            ?sensor a sosa:Sensor .
            ?sensor ioto:usesDataFormat ?dataFormat .
            }
        """, initNs={"sosa": sosa, "ioto": ioto})

        results = []
        for row in self.g.query(query):
            results.append({
                "device": str(row.device),
                "sensor": str(row.sensor),
                "data_format": str(row.dataFormat)
            })
        end_time = time.time()
        execution_time = end_time - start_time
        if self.result_mode=='time':
            return f"{execution_time:.6f} seconds"
        return results
    
    def cat1_qb(self):
        start_time = time.time()
        query = prepareQuery("""
            SELECT ?device ?sensor ?dataFormat ?deviceType
            WHERE {
                ?device a ioto:IoTDevice ;
                        ioto:hasSensor ?sensor .

                ?sensor a sosa:Sensor ;
                        ioto:usesDataFormat ?dataFormat .

                OPTIONAL { ?device a ioto:ModernDevice . BIND("ModernDevice" AS ?deviceType) }
                OPTIONAL { ?device a ioto:LegacyDevice . BIND("LegacyDevice" AS ?deviceType) }
            }
        """, initNs={"sosa": sosa, "ioto": ioto})
        results = []
        for row in self.g.query(query):
            results.append({
                "device": str(row.device),
                "sensor": str(row.sensor),
                "data_format": str(row.dataFormat),
                "device_type": str(row.deviceType)
            })
        end_time = time.time()
        execution_time = end_time - start_time
        if self.result_mode=='time':
            return f"{execution_time:.6f} seconds"
        return results
    
    def cat1_qc(self):
        start_time = time.time()
        query = prepareQuery("""
            SELECT DISTINCT ?device ?standard ?protocol
            WHERE {
            ?device a ioto:IoTDevice .
            OPTIONAL { ?device ioto:hasStandard ?standard . }
            OPTIONAL { ?device ioto:usesProtocol ?protocol .}
            }
        """, initNs={"sosa": sosa, "ioto": ioto})
        results = []
        for row in self.g.query(query):
            results.append({
                "device": str(row.device),
                "standard": str(row.standard) if row.standard else None,
                "protocol": str(row.protocol) if row.protocol else None
            })
        end_time = time.time()
        execution_time = end_time - start_time
        if self.result_mode=='time':
            return f"{execution_time:.6f} seconds"
        return results