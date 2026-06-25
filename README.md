##python3.11 hello
 python3.11 -m venv /home/hadoop/venv-llm
 
 source /home/hadoop/venv-llm/bin/activate
 
 deactivate

# pip install openai-whisper python-multipart pydantic-settings

-One terminal

python3 -m http.server 8081 

--Another terminal

Agent-jalebi>python main.py

http://0.0.0.0:8081/

OR

./start.sh

#restart API
fuser -k 8000/tcp && cd ~/Agent-jalebi/ && python main.py

sudo fuser -k 8080/tcp

sudo lsof -i :8080

##


#PostgreSQL Table
use test;

CREATE TABLE transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    qty INTEGER,
    price NUMERIC(10,2) NOT NULL,
    item VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Suggested Architecture
Microphone
    |
    v
Speech-to-Text (Whisper)
    |
    v
Ollama LLM (Llama 3 / Mistral)
    |
    |--> Extract JSON
    |
    v
Validation Layer
    |
    +--> Save to transactions.txt
    |
    +--> Save to PostgreSQL
Expected JSON from Ollama
{
  "name": "Chandra",
  "qty": 2,
  "price": 20,
  "item": "Samosa"
}
Ollama Prompt
Extract transaction details from the user sentence.

Rules:
1. Return only valid JSON.
2. item and price are mandatory.
3. qty defaults to 1 if not provided.
4. Correct spelling mistakes.
5. Standardize item names.

Output format:

{
  "name": "",
  "qty": 0,
  "price": 0,
  "item": ""
}

User Input:
{{speech_text}}
Sample Python Flow
import uuid
import json
import psycopg2
from datetime import datetime
from ollama import chat

speech_text = "chandra purchased 2 samosa for 20 rupees"

response = chat(
    model="llama3",
    messages=[
        {
            "role": "user",
            "content": f"""
Extract transaction details and return JSON only.

Text: {speech_text}
"""
        }
    ]
)

data = json.loads(response.message.content)

if not data.get("item") or not data.get("price"):
    raise Exception("Item and Price are mandatory")

txn_id = str(uuid.uuid4())

# Save to text file
with open("transactions.txt", "a") as f:
    f.write(
        f"{txn_id},{data['name']},{data['qty']},"
        f"{data['price']},{data['item']},{datetime.now()}\n"
    )

# Save to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="transactions",
    user="postgres",
    password="password"
)

cur = conn.cursor()

cur.execute("""
INSERT INTO transactions
(transaction_id,name,qty,price,item)
VALUES (%s,%s,%s,%s,%s)
""",
(
    txn_id,
    data["name"],
    data["qty"],
    data["price"],
    data["item"]
))

conn.commit()
cur.close()
conn.close()
Example Voice Inputs
Spoken Sentence	Parsed Output
"Chandra bought 2 samosas for 20 rupees"	Name=Chandra, Qty=2, Price=20, Item=Samosa
"Ravi purchased tea 15 rupees"	Name=Ravi, Qty=1, Price=15, Item=Tea
"Ankit 5 mangoes 200 rupees"	Name=Ankit, Qty=5, Price=200, Item=Mango

For a production-grade agent, I would recommend:

Whisper for speech-to-text
Ollama + Llama 3 for extraction
PostgreSQL for storage
FastAPI for APIs
LangGraph for agent orchestration and validation workflows.
