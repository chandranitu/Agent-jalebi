import json
from ollama import chat

class TransactionAgent:
    def __init__(self, model="llama3"):
        self.model = model

    def extract_transaction(self, text: str) -> dict:
        prompt = f"""
Extract transaction details from the user sentence.

Rules:
1. Return only valid JSON.
2. item and price are mandatory.
3. qty defaults to 1 if not provided.
4. Correct spelling mistakes.
5. Standardize item names.

Output format:
{{
  "name": "string or null",
  "qty": integer,
  "price": number,
  "item": "string"
}}

User Input: {text}
"""
        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        content = response.message.content
        
        # Try to find JSON block
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            content = json_match.group(0)
        else:
            # Fallback to code block logic
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
        try:
            data = json.loads(content.strip())
            return data
        except json.JSONDecodeError:
            raise ValueError(f"Failed to extract JSON from response: {content}")

agent = TransactionAgent()
