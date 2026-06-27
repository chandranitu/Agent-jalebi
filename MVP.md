# MVP1
1. Login Authentication 
2. transaction should be based on voice
3. Give sample voice for noise cancellation
4. 




#MVP2
1. 

#Details
Build an Agentic AI system using Ollama. When I speak a transaction, the AI should:

Convert speech to text.
Extract structured fields from the spoken sentence.
Validate that Item and Price are mandatory.
Generate a unique Transaction ID for every entry.
Save the transaction to a text file.
Save the same transaction to a PostgreSQL database.
If the spoken sentence contains grammar mistakes or informal language, the LLM should normalize and structure it correctly.
Example

User speaks:
"Chandra bought 2 samosas for 20 rupees"
OR
2 samosa 20

Structured Output:
Transaction ID	Name	Qty	Price	Item
TXN_20260801_001	Chandra	2	20	Samosa

Text File Entry
Transaction ID: TXN_20260801_001
Name: Chandra
Qty: 2
Price: 20
Item: Samosa
Timestamp: 2026-08-01 10:30:15
----------------------------------

