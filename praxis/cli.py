"""PRAXIS-1 CLI Entry Point (v0.3.0)

This is the main interface for PRAXIS-1.
Users can run the assistant in three modes:
  1. CLI assistant (default)
  2. GPT-4 fallback mode (--fallback)
  3. Autonomous agent mode (--agent)

Each command is processed by a language model (LLM),
converted to a shell command, approved, executed,
and logged to a session file.

Related modules used here:
- praxis.llm.mistral_local → local LLM via Ollama
- praxis.llm.gpt4_api      → optional GPT-4 fallback
- praxis.utils.shell       → shell safety execution
- praxis.utils.logging     → logs all actions to disk
- praxis.agents.agent_core → goal-driven AI agent mode

"""

from __future__ import annotations
import click
from dotenv import load_dotenv

# Load environment variables (.env) for API keys, role, etc.
load_dotenv()

# --- Import core model interfaces and tools ---
from praxis.llm.mistral_local import generate_command as mistral_gen
from praxis.utils.shell import run_command
from praxis.utils.logging import log_entry

# Optional GPT-4 fallback model
try:
    from praxis.llm.gpt4_api import generate_command as gpt4_gen
except ImportError:
    gpt4_gen = None

# -------------------------------
# CLI OPTIONS AND ENTRY FUNCTION
# -------------------------------

@click.command()
@click.option("--debug", is_flag=True, help="Enable debug output.")
@click.option("--fallback", is_flag=True, help="Force GPT-4 instead of local model.")
@click.option("--agent", is_flag=True, help="Run in autonomous agent mode.")
def main(debug: bool, fallback: bool, agent: bool):
    """Main CLI entrypoint. This launches PRAXIS-1 in CLI or Agent mode."""

    click.echo("PRAXIS-1 CLI assistant • type 'exit' to quit.")

    # If --agent flag is used, switch to autonomous agent loop
    if agent:
        from praxis.agents.agent_core import run_agent
        goal = input("Enter your goal for the agent: ").strip()
        run_agent(goal, debug=debug)
        return

    # ----------------------
    # Main CLI input loop
    # ----------------------
    while True:
        user_in = input(">>> ").strip()

        if user_in.lower() in {"exit", "quit"}:
            break

        # STEP 1: Determine model source
        try:
            if fallback:
                # User forced GPT-4 use
                cmd = gpt4_gen(user_in)
                model_used = "GPT-4"
            else:
                # Default: use Mistral locally via Ollama
                cmd = mistral_gen(user_in)
                model_used = "Mistral"
                # If Mistral fails or is unsure, fall back to GPT-4
                if not cmd or "I don't know" in cmd.lower():
                    raise ValueError("Unusable response from Mistral")
        except Exception as e:
            if gpt4_gen:
                click.secho("[Fallback] Using GPT-4…", fg="yellow")
                cmd = gpt4_gen(user_in)
                model_used = "GPT-4"
            else:
                click.secho(f"[Error] {e}", fg="red")
                continue

        if debug:
            click.echo(f"[LLM:{model_used}] Proposed: {cmd}")

        # STEP 2: Ask user to confirm command
        confirm = input(f"[CONFIRM] Run this? → {cmd}  [y/N]: ").strip().lower()
        if confirm != "y":
            click.secho("Command skipped by user.", fg="yellow")
            log_entry("CLI", user_in, cmd, "[skipped by user]")
            continue

        # STEP 3: Run the validated command through our shell wrapper
        result = run_command(cmd)

        # STEP 4: Log all relevant data to a timestamped session file
        log_entry("CLI", user_in, cmd, result or "[no output]")

        # STEP 5: Display result to user
        if result is None:
            click.secho("Blocked for safety. (Not in whitelist.)", fg="red")
        else:
            click.secho(result, fg="green")

# Enable standalone script execution
if __name__ == "__main__":
    main()
