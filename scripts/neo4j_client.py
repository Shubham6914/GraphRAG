# neo4j_client.py
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_driver():
    """
    Create and return a Neo4j driver instance using environment variables.
    """
    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME") 
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
    
    if not all([NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD]):
        raise ValueError("Missing Neo4j connection credentials in environment variables")
    
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    return driver
