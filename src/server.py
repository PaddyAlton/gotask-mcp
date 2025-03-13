# gotask-mcp/src/server.py
"""Defines an MCP server for Task that works with Cursor"""

import subprocess

from json import dumps
from os import chdir
from pathlib import Path

from mcp.server.fastmcp import FastMCP


# context manager for changing the working directory
class ChangeDir:
    """Context manager for changing the working directory"""

    def __init__(self, path: Path):
        """Initialize the context manager"""
        self.path = path
        self.original_path = None

    def __enter__(self):
        """Enter the context manager"""
        self.original_path = Path.cwd()
        chdir(self.path)

    def __exit__(self, exc_type, exc_val, exc_tb):  # noqa: ANN001
        """Exit the context manager"""
        chdir(self.original_path)


# Create a named server
server = FastMCP("gotask", log_level="WARNING")


@server.tool()
def task_list(current_project: str) -> str:
    """
    List all tasks defined in the current project's Taskfile.yml

    The caller should look for their current project in user_info
    and pass the project path to this tool.

    Args:
        current_project: The path to the current project

    Returns:
        A string containing the list of tasks

    """
    with ChangeDir(Path(current_project)):
        result = subprocess.run(  # noqa: S603
            ["task", "--list"],  # noqa: S607
            capture_output=True,
            text=True,
            check=False,
        )
        # if something goes wrong, inform the client
        if result.returncode != 0:
            return result.stderr + result.stdout

        # structure the output and return as a string
        task_dict = {
            ln[0].strip("* "): ln[1].strip()
            for ln in [ln.split(":") for ln in result.stdout.splitlines()]
        }
        output = dumps(task_dict, indent=2)
        return output


@server.tool()
def run_task(current_project: str, task_name: str) -> str:
    """
    Run a specific task. The task_list tool should be used
    before calling this tool to get a list of available tasks.

    Args:
        current_project: the path to the current project
        task_name: the name of the task to run

    Returns:
        STDOUT/STDERR output from the task

    """
    with ChangeDir(Path(current_project)):
        result = subprocess.run(  # noqa: S603
            ["task", task_name],  # noqa: S607
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return result.stderr + result.stdout
        return result.stdout


if __name__ == "__main__":
    # N.B. the best way to run this server is with the MCP CLI
    # uv run --with mcp --directory /path/to/gotask-mcp mcp run /path/to/gotask-mcp/src/cursor_server.py  # noqa: E501
    server.run(transport="stdio")
