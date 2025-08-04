import os
from pathlib import Path

from src.venvalid.dotenv import load_env_file


def test_load_env_file_basic(tmp_path: Path, monkeypatch):
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text("FOO=bar\nBAR=baz")

    monkeypatch.delenv("FOO", raising=False)
    monkeypatch.delenv("BAR", raising=False)

    load_env_file(str(dotenv_path))

    assert os.environ["FOO"] == "bar"
    assert os.environ["BAR"] == "baz"


def test_load_env_file_ignores_comments_and_empty_lines(tmp_path: Path, monkeypatch):
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text(
        """
# This is a comment
FOO=123

BAR=456
# Another comment
"""
    )

    monkeypatch.delenv("FOO", raising=False)
    monkeypatch.delenv("BAR", raising=False)

    load_env_file(str(dotenv_path))

    assert os.environ["FOO"] == "123"
    assert os.environ["BAR"] == "456"


def test_load_env_file_does_not_override_by_default(tmp_path: Path, monkeypatch):
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text("FOO=from_dotenv")

    monkeypatch.setenv("FOO", "from_os")

    load_env_file(str(dotenv_path), override=False)

    assert os.environ["FOO"] == "from_os"


def test_load_env_file_with_override(tmp_path: Path, monkeypatch):
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text("FOO=from_dotenv")

    monkeypatch.setenv("FOO", "from_os")

    load_env_file(str(dotenv_path), override=True)

    assert os.environ["FOO"] == "from_dotenv"


def test_load_env_file_skips_invalid_lines(tmp_path: Path, monkeypatch):
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text(
        """
INVALID_LINE
FOO=ok
"""
    )

    monkeypatch.delenv("FOO", raising=False)

    load_env_file(str(dotenv_path))

    assert os.environ["FOO"] == "ok"
    assert "INVALID_LINE" not in os.environ
