import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_FILE = PROJECT_ROOT / "main.py"


def run_cli(*arguments):
    """Run the CLI and capture its output."""
    return subprocess.run(
        [sys.executable, str(MAIN_FILE), *arguments],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        timeout=10
    )


def test_help_displays_all_commands():
    result = run_cli("--help")

    assert result.returncode == 0
    assert "interactive" in result.stdout
    assert "register" in result.stdout
    assert "login" in result.stdout
    assert "books" in result.stdout
    assert "search" in result.stdout
    assert "borrow" in result.stdout
    assert "return" in result.stdout
    assert "records" in result.stdout


def test_search_help_displays_term_argument():
    result = run_cli("search", "--help")

    assert result.returncode == 0
    assert "--term" in result.stdout


def test_borrow_requires_book_id():
    result = run_cli("borrow")

    assert result.returncode != 0
    assert "--book-id" in result.stderr


def test_return_requires_book_id():
    result = run_cli("return")

    assert result.returncode != 0
    assert "--book-id" in result.stderr


def test_search_requires_term():
    result = run_cli("search")

    assert result.returncode != 0
    assert "--term" in result.stderr


def test_invalid_command_is_rejected():
    result = run_cli("invalid-command")

    assert result.returncode != 0
    assert "invalid choice" in result.stderr.lower()
