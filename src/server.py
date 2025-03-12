# gotask-mcp/src/server.py
"""Defines the MCP server for Task"""

import subprocess

from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from src.utils import load_taskfile

# Create a named server
server = FastMCP("gotask", log_level="WARNING")

# import tasks from Taskfile.yml
all_tasks = load_taskfile()

# some 'metaprogramming' here: we dynamically create a tool for each task.
# The task name is the key for the dictionary, so the command `task <name>`
# is what the function should execute. The value from the dictionary is the
# description of the task, which should become the docstring of the tool.
for task_name, task_desc in all_tasks.items():

    def make_task_runner(name: str, desc: str) -> Callable[[], str]:
        """Create a function that runs the specified task"""

        def run_task() -> str:
            """Run the task and return its output"""
            result = subprocess.run(  # noqa: S603
                ["task", name],  # noqa: S607
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                return result.stderr + result.stdout
            return result.stdout

        # Set the docstring to the task description
        run_task.__doc__ = desc
        return run_task

    # Register the task runner as a tool
    server.tool(name=task_name)(make_task_runner(task_name, task_desc))


if __name__ == "__main__":
    server.run(transport="stdio")
