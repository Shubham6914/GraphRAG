# create_relationships.py
from neo4j import GraphDatabase
import pandas as pd
from neo4j_client import get_driver  # assumes you have a driver setup in neo4j_client.py
from pathlib import Path
# Initialize driver
driver = get_driver()

def create_relationship(node1_label, node1_key, node1_value,
                        node2_label, node2_key, node2_value,
                        relationship_type):
    """
    Core function to create a relationship between two nodes using MERGE.
    """
    query = f"""
    MATCH (a:{node1_label} {{{node1_key}: $node1_value}})
    MATCH (b:{node2_label} {{{node2_key}: $node2_value}})
    MERGE (a)-[r:{relationship_type}]->(b)
    RETURN r
    """
    with driver.session() as session:
        session.run(query, node1_value=node1_value, node2_value=node2_value)

def create_relationships_from_commits(csv_path):
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        # User → Commit
        if pd.notna(row.get('author_id')) and pd.notna(row.get('commit_id')):
            create_relationship('User', 'user_id', row['author_id'],
                                'Commit', 'commit_id', row['commit_id'],
                                'MADE')
        # Commit → Issue
        if pd.notna(row.get('commit_id')) and pd.notna(row.get('issue_id')):
            create_relationship('Commit', 'commit_id', row['commit_id'],
                                'Issue', 'issue_id', row['issue_id'],
                                'ADDRESSES')

def create_relationships_from_issues(csv_path):
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        # Issue → Project
        if pd.notna(row.get('issue_id')) and pd.notna(row.get('project_id')):
            create_relationship('Issue', 'issue_id', row['issue_id'],
                                'Project', 'project_id', row['project_id'],
                                'BELONGS_TO')
        # Issue → Status
        if pd.notna(row.get('issue_id')) and pd.notna(row.get('status_id')):
            create_relationship('Issue', 'issue_id', row['issue_id'],
                                'Status', 'status_id', row['status_id'],
                                'HAS_STATUS')

def create_relationships_from_lastupdated(csv_path):
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        # Issue → LastUpdated
        if pd.notna(row.get('issue_id')) and pd.notna(row.get('update_id')):
            create_relationship('Issue', 'issue_id', row['issue_id'],
                                'LastUpdated', 'update_id', row['update_id'],
                                'TRACKED_BY')

def create_relationships_from_metadata(csv_path):
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        # Issue → Metadata
        if pd.notna(row.get('issue_id')) and pd.notna(row.get('metadata_id')):
            create_relationship('Issue', 'issue_id', row['issue_id'],
                                'Metadata', 'metadata_id', row['metadata_id'],
                                'HAS_METADATA')

def create_relationships_from_projects(csv_path):
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        # Project → User (manager)
        if pd.notna(row.get('project_id')) and pd.notna(row.get('user_id')):
            create_relationship('Project', 'project_id', row['project_id'],
                                'User', 'user_id', row['user_id'],
                                'MANAGED_BY')


if __name__ == "__main__":
    # Get base directory of the project (i.e., ruh_knowledge_graph/)
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    create_relationships_from_commits(f"{DATA_DIR}/commits.csv")
    create_relationships_from_issues(f"{DATA_DIR}/issues.csv")
    create_relationships_from_lastupdated(f"{DATA_DIR}/lastupdated.csv")
    create_relationships_from_metadata(f"{DATA_DIR}/metadata.csv")
    create_relationships_from_projects(f"{DATA_DIR}/projects.csv")

    print("All relationships created successfully!")
    driver.close()
