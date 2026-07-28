import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL = "openai/gpt-oss-20b:free"


def ask_llm(context, question):

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY from the provided context.

If the answer is not available in the context, reply:

"I couldn't find the answer in the provided document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    result = response.json()

    return result["choices"][0]["message"]["content"]