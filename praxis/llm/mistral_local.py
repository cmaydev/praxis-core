"""Very small wrapper around Ollama/Mistral."""
import subprocess, json

SYSTEM_PROMPT = (
    "You are a command-line assistant. Your job is to convert natural language requests "
    "into safe, minimal shell commands. DO NOT explain anything. "
    "DO NOT return any prose. Respond ONLY with the command to execute. "
    "Allowed commands: ls, pwd, whoami, cat, date, echo, and echo > file.txt to write notes. "
    "No pipes, no &&, no sudo, no deletions."
)



OLLAMA_MODEL = "mistral"

def generate_command(user_request: str) -> str:
    """Call ollama with a JSON prompt; return the command string."""
    prompt = {
        "role": "user",
        "content": f"{SYSTEM_PROMPT}\n\nUser: {user_request}"
    }
    completed = subprocess.run(
        ["ollama", "run", OLLAMA_MODEL, json.dumps(prompt)],
        capture_output=True, text=True, check=True,
    )
    return completed.stdout.strip()
