"""Tests for utility functions"""

import pytest

from src.utils import load_taskfile


def test_load_taskfile_file_not_found(tmp_path, monkeypatch):
    """Test that FileNotFoundError is raised when no Taskfile exists"""
    monkeypatch.chdir(tmp_path)
    with pytest.raises(FileNotFoundError) as exc_info:
        load_taskfile()
    assert "No valid Taskfile found" in str(exc_info.value)


def test_load_taskfile_precedence(tmp_path, monkeypatch):
    """Test that Taskfiles are loaded in the correct order of precedence"""
    # Create multiple taskfiles
    taskfile_content = """
    version: '3'
    tasks:
      test:
        desc: Run tests
      build:
        desc: Build project
      deploy:
        cmds:
          - echo "deploying"
    """

    lower_priority = tmp_path / "taskfile.yaml"
    higher_priority = tmp_path / "Taskfile.yml"

    lower_priority.write_text(taskfile_content)
    higher_priority.write_text(taskfile_content)

    monkeypatch.chdir(tmp_path)
    tasks = load_taskfile()

    assert isinstance(tasks, dict)
    assert len(tasks) == 2  # Only tasks with descriptions
    assert tasks["test"] == "Run tests"
    assert tasks["build"] == "Build project"
    assert "deploy" not in tasks  # No description, should be filtered out


def test_load_taskfile_content_parsing(tmp_path, monkeypatch):
    """Test that Taskfile content is correctly parsed and filtered"""
    taskfile_content = """
    version: '3'
    tasks:
      test:
        desc: Run tests
        cmds:
          - pytest
      build:
        cmds:
          - echo "building"
      deploy:
        desc: Deploy to production
        cmds:
          - echo "deploying"
    """

    taskfile = tmp_path / "Taskfile.yml"
    taskfile.write_text(taskfile_content)

    monkeypatch.chdir(tmp_path)
    tasks = load_taskfile()

    assert isinstance(tasks, dict)
    assert len(tasks) == 2
    assert tasks == {"test": "Run tests", "deploy": "Deploy to production"}
