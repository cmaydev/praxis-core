"""Sandboxed shell execution."""
import subprocess, shlex

ALLOWED = {"ls", "pwd", "date", "whoami", "cat", "echo"}

def run_command(cmd: str) -> str | None:
    parts = shlex.split(cmd)
    if not parts or parts[0] not in ALLOWED:
        return None
    try:
        out = subprocess.check_output(parts, text=True, stderr=subprocess.STDOUT)
        return out
    except subprocess.CalledProcessError as exc:
        return exc.output
