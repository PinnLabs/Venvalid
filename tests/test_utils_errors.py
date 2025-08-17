import sys
import types

import src.venvalid.utils_errors as utils_errors


class DummyConsole:
    def __init__(self):
        self.last_message = None

    def print(self, msg):
        self.last_message = msg


def test_pretty_print_error_with_rich(monkeypatch):
    dummy_console = DummyConsole()

    fake_rich_pkg = types.ModuleType("rich")
    fake_rich_pkg.__path__ = []  # mark as package

    fake_console_mod = types.ModuleType("rich.console")
    setattr(fake_console_mod, "Console", lambda: dummy_console)

    monkeypatch.setitem(sys.modules, "rich", fake_rich_pkg)
    monkeypatch.setitem(sys.modules, "rich.console", fake_console_mod)

    utils_errors.pretty_print_error(ValueError("boom"))

    assert dummy_console.last_message is not None
    assert "boom" in dummy_console.last_message


def test_pretty_print_error_without_rich(monkeypatch, capsys):
    monkeypatch.delitem(sys.modules, "rich.console", raising=False)
    monkeypatch.delitem(sys.modules, "rich", raising=False)

    utils_errors.pretty_print_error(ValueError("fail"))

    out = capsys.readouterr().out
    assert "Error: fail" in out
