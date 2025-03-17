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

class QuestionnaryModule5:
    def __init__(self, result_mode, file_path="ioto_ontology_instance.ttl"):
        self.g = Graph()
        self.g.parse(file_path, format="turtle")
        self.g.bind("sosa", sosa)
        self.g.bind("colpri", colpri)
        self.g.bind("ioto", ioto)
        self.result_mode = result_mode
        self.module_name = "Questionnary Module 5: Ethics"

    def mod5_qa(self):
        start_time = time.time()
        query = prepareQuery("""
        """, initNs={"ioto": ioto, "colpri": colpri})

        results = []
        for row in self.g.query(query):
            results.append({
            })
        end_time = time.time()
        execution_time = end_time - start_time
        if self.result_mode=='time':
            return f"{execution_time:.4f} seconds"
        return results
    
    def mod5_qb(self):
        start_time = time.time()
        query = prepareQuery("""
        """, initNs={"colpri": colpri, "ioto": ioto, "ds4iot": ds4iot, "rdfs": RDFS})
        
        results = []
        for row in self.g.query(query):
            results.append({
            })

        end_time = time.time()
        execution_time = end_time - start_time
        if self.result_mode == 'time':
            return f"{execution_time:.4f} seconds"
        return results

    
    def mod5_qc(self):
        start_time = time.time()
        query = prepareQuery("""
            
        """, initNs={"colpri": colpri})
        results = []
        for row in self.g.query(query):
            results.append({              
            })
        end_time = time.time()
        execution_time = end_time - start_time
        if self.result_mode=='time':
            return f"{execution_time:.4f} seconds"
        return results
    
    def mod5_qd(self):
        start_time = time.time()
        query = prepareQuery("""
            
        """, initNs={"colpri": colpri})
        results = []
        for row in self.g.query(query):
            results.append({              
            })
        end_time = time.time()
        execution_time = end_time - start_time
        if self.result_mode=='time':
            return f"{execution_time:.4f} seconds"
        return results