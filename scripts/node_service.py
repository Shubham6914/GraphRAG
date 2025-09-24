# create_nodes.py

from neo4j import GraphDatabase
import pandas as pd
from neo4j_client import get_driver
from pathlib import Path
driver = get_driver()




# Get base directory of the project (i.e., ruh_knowledge_graph/)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"





# -------------------------------
# Utility function to insert nodes
# -------------------------------
def create_node(tx, label, properties):
    """
    Create a node with a given label and properties.
    """
    query = f"CREATE (n:{label} $props)"
    tx.run(query, props=properties)


# -------------------------------
# Functions for each entity
# -------------------------------
def create_users(file_path):
    df = pd.read_csv(file_path)
    with driver.session() as session:
        for _, row in df.iterrows():
            session.execute_write(
                create_node,
                "User",
                {
                    "user_id": row["user_id"],
                    "name": row["name"],
                    "email": row["email"],
                    "role": row["role"],
                },
            )
    print("✅ Users created successfully")


def create_projects(file_path):
    df = pd.read_csv(file_path)
    with driver.session() as session:
        for _, row in df.iterrows():
            session.execute_write(
                create_node,
                "Project",
                {
                    "project_id": row["project_id"],
                    "project_name": row["project_name"],
                    "description": row["description"],
                },
            )
    print("✅ Projects created successfully")


def create_issues(file_path):
    df = pd.read_csv(file_path)
    with driver.session() as session:
        for _, row in df.iterrows():
            session.execute_write(
                create_node,
                "Issue",
                {
                    "issue_id": row["issue_id"],
                    "title": row["title"],
                    "priority": row["priority"],
                    "project_id": row["project_id"],
                },
            )
    print("✅ Issues created successfully")


def create_commits(file_path):
    df = pd.read_csv(file_path)
    with driver.session() as session:
        for _, row in df.iterrows():
            session.execute_write(
                create_node,
                "Commit",
                {
                    "commit_id": row["commit_id"],
                    "message": row["message"],
                    "author_id": row["author_id"],
                    "issue_id": row["issue_id"],
                },
            )
    print("✅ Commits created successfully")


def create_status(file_path):
    df = pd.read_csv(file_path)
    with driver.session() as session:
        for _, row in df.iterrows():
            session.execute_write(
                create_node,
                "Status",
                {
                    "status_id": row["status_id"],
                    "status_name": row["status_name"],
                },
            )
    print("✅ Status created successfully")


def create_lastupdated(file_path):
    df = pd.read_csv(file_path)
    with driver.session() as session:
        for _, row in df.iterrows():
            session.execute_write(
                create_node,
                "LastUpdated",
                {
                    "update_id": row["update_id"],
                    "issue_id": row["issue_id"],
                    "last_updated": row["last_updated"],
                },
            )
    print("✅ LastUpdated created successfully")


def create_metadata(file_path):
    df = pd.read_csv(file_path)
    with driver.session() as session:
        for _, row in df.iterrows():
            session.execute_write(
                create_node,
                "Metadata",
                {
                    "metadata_id": row["metadata_id"],
                    "issue_id": row["issue_id"],
                    "labels": row["labels"],
                    "created_by": row["created_by"],
                    "priority": row["priority"],
                },
            )
    print("✅ Metadata created successfully")


# -------------------------------
# Main runner
# -------------------------------
if __name__ == "__main__":
    create_users(DATA_DIR / "users.csv")
    create_projects(DATA_DIR / "projects.csv")
    create_issues(DATA_DIR / "issues.csv")
    create_commits(DATA_DIR / "commits.csv")
    create_status(DATA_DIR / "status.csv")
    create_lastupdated(DATA_DIR / "lastupdated.csv")
    create_metadata(DATA_DIR / "metadata.csv")

    driver.close()
    print("🎉 All nodes created successfully!")