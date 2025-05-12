"""Simple memory class for tracking agent task context."""

class Memory:
    def __init__(self, goal: str = ""):
        self.goal = goal
        self.log = []

    def add_step(self, command: str):
        self.log.append(command)

    def __str__(self):
        return "\n".join(self.log)
