"""PRAXIS-1 Autonomous Agent Core (v0.3.0)

This module allows PRAXIS-1 to interpret high-level user goals
and autonomously break them into shell commands.

Each step is:
  - Proposed by the LLM
  - Confirmed by the user (y/N)
  - Executed safely
  - Logged to a session file

Related modules:
- praxis.llm.mistral_local → generates shell steps
- praxis.utils.shell       → executes validated shell commands
- praxis.utils.logging     → writes logs to file
- praxis.agents.memory     → simple step history tracker
"""

from praxis.llm.mistral_local import generate_command
from praxis.utils.shell import run_command
from praxis.utils.logging import log_entry
from praxis.agents.memory import Memory

def run_agent(goal: str, debug: bool = False) -> None:
    """Main loop for autonomous agent mode."""

    memory = Memory(goal=goal)

    print(f"[AGENT] Starting goal execution: {goal}")

    # Limit to max 5 steps unless explicitly continued
    while len(memory.log) < 5:
        # Prompt LLM to suggest next shell step
        step_prompt = f"Given the goal: '{goal}' and history: {memory.log}, what is the next safe shell command?"
        cmd = generate_command(step_prompt)
        memory.add_step(cmd)

        if debug:
            print(f"[AGENT] Proposed command: {cmd}")

        # Confirm command before running
        confirm = input(f"[AGENT] Approve this step? → {cmd}  [y/N]: ").strip().lower()
        if confirm != "y":
            print("[AGENT] Step skipped by user.")
            log_entry("AGENT", goal, cmd, "[skipped by user]")
            break

        # Execute and log
        result = run_command(cmd)
        log_entry("AGENT", goal, cmd, result or "[no output]")

        # Display output
        if result is None:
            print("[AGENT] Blocked or failed.")
            break
        else:
            print(result)

        # Optional exit condition
        if "completed" in result.lower():
            print("[AGENT] Task marked as complete.")
            break

    print("[AGENT] Session ended.")
