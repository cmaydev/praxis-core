"""Agent Core — interprets high-level goals and breaks them into steps."""
from praxis.llm.mistral_local import generate_command
from praxis.utils.shell import run_command
from praxis.agents.memory import Memory

def run_agent(goal: str, debug: bool = False) -> None:
    memory = Memory(goal=goal)

    while True:
        step_prompt = f"Given the goal: '{goal}', and history: {memory.log}, what is the next shell command to run?"
        cmd = generate_command(step_prompt)
        memory.add_step(cmd)

        if debug:
            print(f"[AGENT] Next Command: {cmd}")

        result = run_command(cmd)
        if result is None:
            print("Command blocked or failed.")
            break

        print(result)
        if "completed" in result.lower() or len(memory.log) > 5:
            print("[AGENT] Task appears complete.")
            break
