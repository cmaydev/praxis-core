"""Simple session logger for PRAXIS-1."""
import os
from datetime import datetime

LOG_DIR = os.path.expanduser("~/praxis-core/praxis/data/logs")
os.makedirs(LOG_DIR, exist_ok=True)

SESSION_FILE = os.path.join(
    LOG_DIR, datetime.now().strftime("%Y-%m-%d_%H%M%S") + ".log"
)

def log_entry(source: str, user_input: str, command: str, output: str):
    with open(SESSION_FILE, "a") as f:
        f.write(f"[{source}] INPUT: {user_input}\n")
        f.write(f"[{source}] CMD:   {command}\n")
        f.write(f"[{source}] OUT:   {output}\n")
        f.write("-" * 40 + "\n")
