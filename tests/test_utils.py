"""Tests for utility functions"""

from pathlib import Path

import pytest

from src.utils import ChangeDir, load_taskfile


class TestLoadTaskfile:
    """Tests for the load_taskfile function"""

    def test_file_not_found(self, tmp_path, monkeypatch):
        """Test that FileNotFoundError is raised when no Taskfile exists"""
        monkeypatch.chdir(tmp_path)
        with pytest.raises(FileNotFoundError) as exc_info:
            load_taskfile()
        assert "No valid Taskfile found" in str(exc_info.value)

    def test_precedence(self, tmp_path, monkeypatch):
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

    def test_content_parsing(self, tmp_path, monkeypatch):
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


class TestChangeDir:
    """Tests for the ChangeDir context manager"""

    def test_changes_directory(self, tmp_path):
        """Test that ChangeDir successfully changes to the target directory"""
        original_dir = Path.cwd()
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        with ChangeDir(test_dir):
            assert Path.cwd() == test_dir

        assert Path.cwd() == original_dir

    def test_restores_on_exception(self, tmp_path):
        """Test that ChangeDir restores the original directory after an exception"""
        original_dir = Path.cwd()
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        def raise_error():
            with ChangeDir(test_dir):
                assert Path.cwd() == test_dir
                error_msg = "Directory change test exception"
                raise RuntimeError(error_msg)

        with pytest.raises(RuntimeError):
            raise_error()

        assert Path.cwd() == original_dir

    def test_nonexistent_directory(self, tmp_path):
        """Test that ChangeDir raises an error for non-existent directories"""
        nonexistent_dir = tmp_path / "does_not_exist"

        def attempt_change():
            with ChangeDir(nonexistent_dir):
                pass  # Should not reach here

        with pytest.raises(FileNotFoundError):
            attempt_change()
