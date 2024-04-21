import streamlit as st  
from rdflib import Graph, Namespace, Literal, URIRef  
from rdflib.namespace import RDF, RDFS  
from rdflib.plugins.stores.sparqlstore import SPARQLStore  
from rdflib_sqlalchemy import registerplugins  
from sqlalchemy import create_engine  
  
# Initialize the graph and the namespaces  
graph = Graph()  
ns = Namespace("http://example.com/")  
registerplugins()  
engine = create_engine('sqlite:///graph.db')  
graph.open(engine)  
  
# Define the node types  
node_types = ["person", "IP", "domain", "organization", "address", "geolocation", "email", "phone number"]  
  
# Define the investigation case class  
class InvestigationCase:  
    def __init__(self, name):  
        self.name = name  
        self.nodes = []  
  
    def add_node(self, node):  
        self.nodes.append(node)  
  
# Define the node class  
class Node:  
    def __init__(self, name, node_type, case):  
        self.name = name  
        self.node_type = node_type  
        self.case = case  
  
    def to_rdf(self):  
        node_uri = ns[self.name.replace(" ", "_")]  
        graph.add((node_uri, RDF.type, ns[self.node_type]))  
        graph.add((node_uri, RDFS.label, Literal(self.name)))  
  
        case_uri = ns[self.case.name.replace(" ", "_")]  
        graph.add((node_uri, ns.belongs_to, case_uri))  
  
    def __str__(self):  
        return f"{self.name} ({self.node_type})"  
  
# Define the edge class  
class Edge:  
    def __init__(self, source, target):  
        self.source = source  
        self.target = target  
  
    def to_rdf(self):  
        source_uri = ns[self.source.name.replace(" ", "_")]  
        target_uri = ns[self.target.name.replace(" ", "_")]  
  
        graph.add((source_uri, ns.linked_to, target_uri))  
  
    def __str__(self):  
        return f"{self.source} -> {self.target}"  
  
# Define the Streamlit app  
def app():  
    st.title("Investigation Graph")  
  
    # Create a new investigation case  
    def create_case():  
        name = st.text_input("Enter the name of the investigation case:")  
        case = InvestigationCase(name)  
        return case  
  
    # Create a new node  
    def create_node():  
        name = st.text_input("Enter the name of the node:")  
        node_type = st.selectbox("Select the type of the node:", node_types)  
        case = st.selectbox("Select the investigation case:", [c.name for c in cases])  
        case = next((c for c in cases if c.name == case), None)  
        node = Node(name, node_type, case)  
        return node  
  
    # Create a new edge  
    def create_edge():  
        source = st.selectbox("Select the source node:", [n.name for n in nodes])  
        source = next((n for n in nodes if n.name == source), None)  
        target = st.selectbox("Select the target node:", [n.name for n in nodes])  
        target = next((n for n in nodes if n.name == target), None)  
