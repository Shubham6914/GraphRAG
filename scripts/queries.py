
# queries.py
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
"""
Central place to run Cypher queries.

Keeps Neo4j logic separate.
"""
# Load Neo4j credentials
load_dotenv()
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

def run_cypher(query: str):
    """
    Executes a Cypher query and returns the results.
    """
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]
