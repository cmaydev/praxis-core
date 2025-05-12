"""GPT-4 fallback using new OpenAI SDK (>=1.0)."""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = (
    "You are a helpful system-command assistant. "
    "Respond with a safe, minimal shell command that fulfills the user's request. "
    "Only output the command, no extra commentary. "
   
)

def generate_command(user_request: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_request}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()
