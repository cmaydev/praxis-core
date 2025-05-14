"""Sandboxed shell execution."""
import subprocess, shlex
from praxis.utils.config import settings

ALLOWED = {"ls", "pwd", "date", "whoami", "cat", "echo"}

def run_command(cmd: str) -> str | None:
    parts = shlex.split(cmd)

    if ">" in cmd and cmd.strip().startswith("echo "):
        if settings.user_role not in {"admin", "developer"}:
            return "[ERROR] Insufficient privileges to write files."

        try:
            parts = cmd.split(">", 1)
            content = parts[0].replace("echo", "").strip().strip('"\'')
            filename = parts[1].strip()
            with open(filename, "w") as f:
                f.write(content + "\n")
            return f"[File written: {filename}]"
        except Exception as e:
            return f"[Error writing file: {e}]"

    if not parts or parts[0] not in ALLOWED:
        return None

    try:
        out = subprocess.check_output(parts, text=True, stderr=subprocess.STDOUT)
        return out
    except subprocess.CalledProcessError as exc:
        return exc.output


