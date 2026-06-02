import psycopg2
from datetime import datetime
import os
import uuid

# Configuration from ReadMeJalebi.md
DB_CONFIG = {
    "host": "localhost",
    "database": "test",
    "user": "postgres",
    "password": "postgres"
}

TXT_FILE = "transactions.txt"

def save_to_txt(txn_id, data):
    with open(TXT_FILE, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"Transaction ID: {txn_id}\nName: {data.get('name')}\nQty: {data.get('qty')}\nPrice: {data.get('price')}\nItem: {data.get('item')}\nTimestamp: {timestamp}\n----------------------------------\n"
        f.write(line)

def save_to_postgres(txn_id, data):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO transactions (transaction_id, name, qty, price, item)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            txn_id,
            data.get("name"),
            data.get("qty", 1),
            data.get("price"),
            data.get("item")
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"Successfully saved to Postgres: {txn_id}")
    except Exception as e:
        print(f"Error saving to Postgres: {e}")
        # We don't raise here to allow the text file save to be the primary success indicator if DB fails
        # but in a real app we might want more robust error handling.

def get_history(limit=10):
    """Fetch recent transactions from Postgres or fall back to text file?"""
    # For now, let's try to fetch from Postgres
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT transaction_id, name, qty, price, item, created_at FROM transactions ORDER BY created_at DESC LIMIT %s", (limit,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        history = []
        for r in rows:
            history.append({
                "id": r[0],
                "name": r[1],
                "qty": r[2],
                "price": float(r[3]),
                "item": r[4],
                "created_at": r[5].isoformat()
            })
        return history
    except Exception as e:
        print(f"Could not fetch from Postgres: {e}")
        return []

def save_transaction(data):
    txn_id = f"TXN_{datetime.now().strftime('%Y%m%d')}_{str(uuid.uuid4())[:8]}"
    save_to_txt(txn_id, data)
    save_to_postgres(txn_id, data)
    return txn_id
