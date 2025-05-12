"""Command-line entrypoint for PRAXIS-1 (v0.2.0) with GPT-4 fallback."""
from __future__ import annotations
import os
import click
from dotenv import load_dotenv
from praxis.llm.mistral_local import generate_command as mistral_gen
from praxis.utils.shell import run_command

# Optional GPT-4 fallback
try:
    from praxis.llm.gpt4_api import generate_command as gpt4_gen
except ImportError:
    gpt4_gen = None

load_dotenv()


@click.command()
@click.option("--debug", is_flag=True, help="Enable debug output.")
@click.option("--fallback", is_flag=True, help="Force GPT-4 instead of local model.")
def main(debug: bool, fallback: bool):
    click.echo("PRAXIS-1 CLI assistant • type 'exit' to quit.")

    while True:
        user_in = input(">>> ").strip()
        if user_in.lower() in {"exit", "quit"}:
            break

        # 1️⃣ Choose model
        try:
            if fallback:
                cmd = gpt4_gen(user_in)
            else:
                cmd = mistral_gen(user_in)
                if not cmd or "I don't know" in cmd.lower():
                    raise ValueError("Unusable response from Mistral")
        except Exception as e:
            if gpt4_gen:
                click.secho("[Fallback] Using GPT-4…", fg="yellow")
                cmd = gpt4_gen(user_in)
            else:
                click.secho(f"[Error] {e}", fg="red")
                continue

        if debug:
            click.echo(f"[LLM] Proposed: {cmd}")

        # 2️⃣ Execute command
        result = run_command(cmd)
        if result is None:
            click.secho("Blocked for safety. (Not in whitelist.)", fg="red")
        else:
            click.secho(result, fg="green")


if __name__ == "__main__":
    main()
