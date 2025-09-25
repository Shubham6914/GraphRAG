# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from query_analyzer import generate_cypher
from queries import run_cypher
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class RequestyLLM:
    def __init__(self):
        self.api_key = os.getenv("REQUESTY_API_KEY")
        if not self.api_key:
            raise ValueError("Missing REQUESTY_API_KEY in .env")

        # Initialize OpenAI client with Requesty router
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://router.requesty.ai/v1"
        )

    def humanize_answer(self, user_query: str, records: list) -> str:
        """
        Convert raw Neo4j results into a human-readable answer using Requesty LLM.
        """
        result_text = str(records) if records else "No data found."

        prompt = f"""
        User asked: "{user_query}"
        Neo4j returned: {result_text}
        Please generate a concise, human-readable answer in natural English.
        """

        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-4o",  # Requesty requires provider/model format
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that converts database query results into natural language."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=800,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"⚠️ LLM error: {str(e)}"


# FastAPI app
app = FastAPI(title="Neo4j + Requesty Q&A")
llm = RequestyLLM()


class UserQuery(BaseModel):
    query: str


@app.post("/ask")
def ask_question(user_query: UserQuery):
    try:
        # Step 1: Convert user query into Cypher
        cypher_query = generate_cypher(user_query.query)

        # Step 2: Run Cypher query
        records = run_cypher(cypher_query)

        # Step 3: Humanize the response
        answer = llm.humanize_answer(user_query.query, records)

        return {
            "query": user_query.query,
            "cypher": cypher_query,
            "raw_results": records,
            "answer": answer,
        }

    except Exception as e:
        return {"error": str(e)}
