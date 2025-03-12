# src/utils.py
"""Utility functions for the MCP server"""

from pathlib import Path

from saneyaml import load as yaml_load


def load_taskfile() -> dict:
    """Load the Taskfile.yml file"""
    current_dir = Path.cwd()
    valid_names = [  # in the proper order of precedence
        "Taskfile.yml",
        "taskfile.yml",
        "Taskfile.yaml",
        "taskfile.yaml",
        "Taskfile.dist.yml",
        "taskfile.dist.yml",
        "Taskfile.dist.yaml",
        "taskfile.dist.yaml",
    ]
    for name in valid_names:
        taskfile_path = current_dir / name
        if taskfile_path.exists():
            break
    else:  # triggered if the loop completes without a break
        emsg = "No valid Taskfile found in current working directory"
        raise FileNotFoundError(emsg)

    with taskfile_path.open() as f:
        taskfile_data = yaml_load(f)

    # get only the tasks with a description
    # and drop all other information
    tasks = {
        key: val.get("desc")
        for key, val in taskfile_data["tasks"].items()
        if val.get("desc") is not None
    }
    return tasks
