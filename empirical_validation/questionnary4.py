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

class QuestionnaryModule4:
    def __init__(self, result_mode, file_path="ioto_ontology_instance.ttl"):
        self.g = Graph()
        self.g.parse(file_path, format="turtle")
        self.g.bind("sosa", sosa)
        self.g.bind("colpri", colpri)
        self.g.bind("ioto", ioto)
        self.result_mode = result_mode
        self.module_name = "Questionnary Module 4:Environment Awareness"

    def mod4_qa(self):
        start_time = time.time()
        query = prepareQuery("""
            SELECT DISTINCT ?sensor ?observedFactor ?energyForm
            WHERE {
                ?sensor a sosa:Sensor ;
                        sosa:observes ?observedFactor .

                OPTIONAL { 
                    ?observedFactor ioto:associatedEnergyForm ?energyForm .
                }
            }
        """, initNs={"ioto": ioto, "sosa": sosa})

        results = []
        for row in self.g.query(query):
            results.append({
                "sensor": row.sensor,
                "observedFactor": row.observedFactor,
                "energyForm": row.energyForm
            })
        end_time = time.time()
        execution_time = end_time - start_time
        if self.result_mode=='time':
            return f"{execution_time:.4f} seconds"
        return results
    
    def mod4_qb(self):
        start_time = time.time()
        query = prepareQuery("""
            SELECT ?sensor ?observedProperty ?currentValue ?resultTime
            WHERE {
                ?obs a sosa:Observation ;
                    sosa:madeBySensor ?sensor ;
                    sosa:observedProperty ?observedProperty ;
                    sosa:hasSimpleResult ?currentValue ;
                    sosa:resultTime ?resultTime .
            }
            ORDER BY DESC(?resultTime)
        """, initNs={"sosa": sosa})
        
        results = []
        for row in self.g.query(query):
            results.append({
                "sensor": row.sensor,
                "observedProperty": row.observedProperty,
                "currentValue": row.currentValue,
                "resultTime": row.resultTime
            })

        end_time = time.time()
        execution_time = end_time - start_time
        if self.result_mode == 'time':
            return f"{execution_time:.4f} seconds"
        return results

    
    def mod4_qc(self):
        start_time = time.time()
        query = prepareQuery("""
            SELECT ?evaluation ?property ?metric ?value
            WHERE {
                ?evaluation a seas:Evaluation ;
                        seas:evaluationOf ?property ;
                        seas:evaluatedValue ?value ;
                        ioto:relatesToMetric ?metric .
            }          
        """, initNs={"ioto": ioto, "sosa": sosa, "seas": seas})
        results = []
        for row in self.g.query(query):
            results.append({      
                "evaluation": row.evaluation,
                "property": row.property,
                "metric": row.metric,
                "value": row.value   
            })
        end_time = time.time()
        execution_time = end_time - start_time
        if self.result_mode=='time':
            return f"{execution_time:.4f} seconds"
        return results
    
    def mod4_qd(self):
        start_time = time.time()
        query = prepareQuery("""
        SELECT DISTINCT ?controlAction ?energyForm
        WHERE {
            ?controlAction a ioto:ControlAction ;
                        ioto:adjusts ?energyForm .
            ?energyForm a seas:EnergyForm .
        }            
        """, initNs={"ioto": ioto, "seas": seas})
        results = []
        for row in self.g.query(query):
            results.append({      
                "controlAction": row.controlAction,
                "energyForm": row.energyForm        
            })
        end_time = time.time()
        execution_time = end_time - start_time
        if self.result_mode=='time':
            return f"{execution_time:.4f} seconds"
        return results