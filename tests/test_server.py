"""Tests for utility functions"""

from pathlib import Path

import pytest

from src.server import ChangeDir


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
