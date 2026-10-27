
import json

import pytest

from utils.json_manager import JSONManager


def test_save_and_load_json(tmp_path):
    """Test saving data and loading it again."""
    file_path = tmp_path / "books.json"
    data = [
        {
            "book_id": "B001",
            "title": "Python Programming",
            "author": "Mark Smith",
            "category": "Programming",
            "is_available": True
        }
    ]

    JSONManager.save(str(file_path), data)
    loaded_data = JSONManager.load(str(file_path))

    assert loaded_data == data


def test_load_missing_file_returns_empty_list(tmp_path):
    """Test that a missing JSON file returns an empty list."""
    file_path = tmp_path / "missing.json"

    result = JSONManager.load(str(file_path))

    assert result == []


def test_load_malformed_json_returns_empty_list(
    tmp_path, capsys
):
    """Test handling of invalid JSON."""
    file_path = tmp_path / "invalid.json"
    file_path.write_text("{invalid json", encoding="utf-8")

    result = JSONManager.load(str(file_path))

    assert result == []
    assert "invalid JSON" in capsys.readouterr().out


def test_load_empty_json_array(tmp_path):
    """Test loading an empty JSON array."""
    file_path = tmp_path / "empty.json"
    file_path.write_text("[]", encoding="utf-8")

    result = JSONManager.load(str(file_path))

    assert result == []


def test_save_creates_valid_json(tmp_path):
    """Test that saved content is valid JSON."""
    file_path = tmp_path / "users.json"
    data = [{"username": "john", "role": "student"}]

    JSONManager.save(str(file_path), data)

    with file_path.open("r", encoding="utf-8") as file:
        saved_data = json.load(file)

    assert saved_data == data


def test_load_read_error_returns_empty_list(
    tmp_path, monkeypatch, capsys
):
    """Test handling of an operating-system read error."""
    file_path = tmp_path / "books.json"
    file_path.write_text("[]", encoding="utf-8")

    original_open = open

    def failing_open(filename, *args, **kwargs):
        if str(filename) == str(file_path):
            raise OSError("Simulated read error")
        return original_open(filename, *args, **kwargs)

    monkeypatch.setattr("builtins.open", failing_open)

    result = JSONManager.load(str(file_path))

    assert result == []
    assert "Simulated read error" in capsys.readouterr().out


def test_save_write_error_is_handled(
    tmp_path, monkeypatch, capsys
):
    """Test handling of an operating-system write error."""
    file_path = tmp_path / "books.json"

    original_open = open

    def failing_open(filename, *args, **kwargs):
        if str(filename) == str(file_path):
            raise OSError("Simulated write error")
        return original_open(filename, *args, **kwargs)

    monkeypatch.setattr("builtins.open", failing_open)

    JSONManager.save(str(file_path), [{"book_id": "B001"}])

    assert "Simulated write error" in capsys.readouterr().out
