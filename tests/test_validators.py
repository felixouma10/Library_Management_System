
import pytest

from utils.validators import (
    validate_not_empty,
    validate_password,
    get_menu_choice
)


def test_validate_not_empty_accepts_valid_text():
    result = validate_not_empty("  John  ", "Name")

    assert result == "John"


def test_validate_not_empty_rejects_empty_string():
    with pytest.raises(ValueError, match="Name cannot be empty"):
        validate_not_empty("", "Name")


def test_validate_not_empty_rejects_whitespace():
    with pytest.raises(ValueError, match="Name cannot be empty"):
        validate_not_empty("   ", "Name")


def test_validate_password_accepts_four_characters():
    assert validate_password("abcd") == "abcd"


def test_validate_password_accepts_long_password():
    password = "securepassword123"

    assert validate_password(password) == password


def test_validate_password_rejects_short_password():
    with pytest.raises(
        ValueError,
        match="at least 4 characters"
    ):
        validate_password("abc")


def test_get_menu_choice_accepts_valid_choice(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "2")

    assert get_menu_choice(1, 3) == 2


def test_get_menu_choice_rejects_out_of_range_then_retries(
    monkeypatch, capsys
):
    answers = iter(["5", "2"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(answers)
    )

    result = get_menu_choice(1, 3)

    assert result == 2
    assert "between 1 and 3" in capsys.readouterr().out


def test_get_menu_choice_rejects_non_numeric_then_retries(
    monkeypatch, capsys
):
    answers = iter(["hello", "1"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(answers)
    )

    result = get_menu_choice(1, 3)

    assert result == 1
    assert "Invalid input" in capsys.readouterr().out
