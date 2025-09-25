# Neo4j + FastAPI + OpenAI (via Requesty.ai)

This project allows users to ask **natural language questions** about a Neo4j graph.  
The system automatically:
1. Converts the question into a **Cypher query** using OpenAI (proxied through [Requesty.ai](https://requesty.ai/)).
2. Executes the Cypher query on a **Neo4j database**.
3. Converts the raw results into a **human-readable answer**.

---

## ⚡ Features
- Accepts **natural language questions** via a REST API.
- Uses **OpenAI (through Requesty.ai)** to generate Cypher queries.
- Executes queries on **Neo4j**.
- Uses AI to return **concise, human-friendly answers**.
- Built with **FastAPI** for speed and easy API integration.

---

## 🛠️ Tech Stack
- **Python 3.9+**
- **FastAPI** – Web framework
- **Neo4j** – Graph database
- **Requesty.ai + OpenAI SDK** – Natural language to Cypher & humanized answers
- **dotenv** – Environment variable management

---

### 1️⃣ Clone the repo

 git clone https://github.com/your-username/neo4j-fastapi-openai.git
cd neo4j-fastapi-openai


### Set up environment variables

# Requesty API
REQUESTY_API_KEY=your_requesty_api_key

# Neo4j Database
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password


 ### 🚀 Run the server
uvicorn app:app --reload


```bash
