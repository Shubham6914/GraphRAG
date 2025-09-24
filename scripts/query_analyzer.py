
"""
Accept user query (natural language).

Build a prompt describing your Neo4j graph schema + relationships.

Call OpenAI API to generate a Cypher query.

Return the Cypher query string.
"""
# query_analyzer.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("REQUESTY_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://router.requesty.ai/v1"  # Requesty.ai endpoint
)


GRAPH_SCHEMA = """
Graph Entities:
- User(user_id, name, email, role)
- Project(project_id, project_name, description)
- Issue(issue_id, title, priority, project_id)
- Commit(commit_id, message, author_id, issue_id)
- Status(status_id, status_name)
- LastUpdated(update_id, issue_id, last_updated)
- Metadata(metadata_id, issue_id, labels, created_by, priority)

Relationships (directed):
- User-MADE->Commit
- Commit-ADDRESSES->Issue
- Issue-BELONGS_TO->Project
- Issue-HAS_STATUS->Status
- Issue-TRACKED_BY->LastUpdated
- Issue-HAS_METADATA->Metadata
- Project-MANAGED_BY->User

Example Queries:
1. Which project is Yara Kim working on?
MATCH (u:User {name:'Yara Kim'})-[:MADE]->(:Commit)-[:ADDRESSES]->(i:Issue)-[:BELONGS_TO]->(p:Project) RETURN p;

2. What is the status of Issue I1?
MATCH (i:Issue {issue_id:'I1'})-[:HAS_STATUS]->(s:Status) RETURN s;

3. Who made commit C1?
MATCH (c:Commit {commit_id:'C1'})<-[:MADE]-(u:User) RETURN u;
"""

def generate_cypher(user_question: str) -> str:
    """
    Converts a natural language question to a precise Cypher query using OpenAI.
    """
    prompt = f"""
You are an expert in Neo4j. Use the following schema and relationships to generate an exact Cypher query.
Do NOT invent any entities or relationships. Use only the given labels and relationships.
Return only the Cypher query, do NOT explain.

Graph Schema:
{GRAPH_SCHEMA}

User Question: "{user_question}"
"""
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role":"system", "content":"You are a Neo4j expert assistant that converts questions into Cypher queries."},
            {"role":"user", "content": prompt}
        ],
        temperature=0
    )

    cypher_query = response.choices[0].message.content.strip()
    return cypher_query
