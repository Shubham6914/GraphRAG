# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from query_analyzer import generate_cypher
from queries import run_cypher
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load OpenAI key
load_dotenv()

api_key = os.getenv("REQUESTY_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://router.requesty.ai/v1"  # Requesty.ai endpoint
)

app = FastAPI(title="Neo4j + OpenAI Q&A")

class UserQuery(BaseModel):
    query: str

def humanize_answer(user_query: str, records: list) -> str:
    """
    Convert raw Neo4j results into a human-readable answer using OpenAI.
    """
    # Convert records to string for context
    result_text = str(records) if records else "No data found."
    
    prompt = f"""
    User asked: "{user_query}"
    Neo4j returned: {result_text}
    Please generate a concise, human-readable answer in natural English.
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role":"system", "content":"You are a helpful assistant that converts database query results into natural language."},
            {"role":"user", "content": prompt}
        ],
        temperature=0
    )
    
    humanized = response.choices[0].message.content.strip()
    return humanized

@app.post("/ask")
def ask_question(user_query: UserQuery):
    try:
        # Step 1: Convert user question to Cypher
        cypher_query = generate_cypher(user_query.query)
        
        # Step 2: Execute Cypher query in Neo4j
        records = run_cypher(cypher_query)
        
        # Step 3: Convert results to human-readable answer
        answer = humanize_answer(user_query.query, records)
        
        return {"query": user_query.query, "cypher": cypher_query, "answer": answer}
    
    except Exception as e:
        return {"error": str(e)}
