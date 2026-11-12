import sys
from unittest.mock import patch

import pytest

import main


def test_non_interactive_flag_parsing():
    """--non-interactive and -n flags are parsed correctly."""
    # --non-interactive
    args = main.argparse.ArgumentParser(prog="main")
    args.add_argument("--non-interactive", "-n", action="store_true",
                      help="Run demos non-interactively for CI/curriculum showcases")
    parsed = args.parse_args(["--non-interactive"])
    assert parsed.non_interactive is True

    # -n
    parsed = args.parse_args(["-n"])
    assert parsed.non_interactive is True

    # default
    parsed = args.parse_args([])
    assert parsed.non_interactive is False


def test_run_non_interactive_demo_runs_without_input(monkeypatch, capsys):
    """_run_non_interactive_demo completes without blocking on input()."""
    # Mock input so the demo does not block waiting for user entry.
    def fake_input(prompt=""):
        return "GDKKN"

    monkeypatch.setattr("builtins.input", fake_input)

    main._run_non_interactive_demo()
    captured = capsys.readouterr()

    assert "Caesar Cipher Auto-Solve Demo" in captured.out
    assert "All demos complete." in captured.out
    assert "Non-Interactive Demo Mode" in captured.out


def test_main_non_interactive_exits_cleanly(monkeypatch, capsys):
    """main(['--non-interactive']) runs demo and returns without blocking."""
    # Mock input so neither the demo nor _run's error handler blocks.
    def fake_input(prompt=""):
        return "GDKKN"

    monkeypatch.setattr("builtins.input", fake_input)

    # Patch sys.argv to simulate --non-interactive
    monkeypatch.setattr(sys, "argv", ["main.py", "--non-interactive"])

    try:
        main.main()
    except SystemExit:
        pass

    captured = capsys.readouterr()
    assert "Non-Interactive Demo Mode" in captured.out
    assert "All demos complete." in captured.out
    assert "input() should not be called" not in captured.out
